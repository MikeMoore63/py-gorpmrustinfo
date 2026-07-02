package main

import "C"

import (
	"debug/buildinfo"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"golang.org/x/mod/modfile"

	"github.com/glebarez/go-sqlite"
	"github.com/jinzhu/copier"
	rpmdb "github.com/knqyf263/go-rpmdb/pkg"
	rustaudit "github.com/rust-secure-code/go-rustaudit"
)

type packageInfo struct {
	Epoch           *int
	Name            string
	Version         string
	Release         string
	Arch            string
	SourceRpm       string
	Size            int
	License         string
	Vendor          string
	Modularitylabel string
	Summary         string
	PGP             string
	SigMD5          string
	RSAHeader       string
	InstallTime     int
	BaseNames       []string
	DirIndexes      []int32
	DirNames        []string
	FileSizes       []int32
	FileDigests     []string
	FileModes       []uint16
	FileFlags       []int32
	UserNames       []string
	GroupNames      []string
	Provides        []string
	Requires        []string
}

//export getrpmdbInfo
func getrpmdbInfo(fileNameIn *C.char) *C.char {
	return C.CString(getrpmdbInfoInternal(C.GoString(fileNameIn)))
}

//export getrustAudit
func getrustAudit(fileNameIn *C.char) *C.char {
	return C.CString(getrustAuditInternal(C.GoString(fileNameIn)))
}

//export getgobuildinfo
func getgobuildinfo(fileNameIn *C.char) *C.char {
	return C.CString(getGoBuildInfoInternal(C.GoString(fileNameIn)))
}

//export getgomod
func getgomod(fileNameIn *C.char) *C.char {
	return C.CString(getGoMod(C.GoString(fileNameIn)))
}

func main() {}

func getrpmdbInfoInternal(fileName string) string {
	returnValue := `{ "error" : "Unknown" }`
	db, err := rpmdb.Open(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf(`{ "error": "path error:%v" }`, fileName)
		} else {
			returnValue = fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
		}
		return returnValue
	}

	pkgList, err := db.ListPackages()
	if err != nil {
		return fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
	}

	mySlice := []packageInfo{}
	for _, pkg := range pkgList {
		rpmdbPkg := new(packageInfo)
		copier.Copy(rpmdbPkg, *pkg)
		mySlice = append(mySlice, *rpmdbPkg)
	}
	data, _ := json.Marshal(mySlice)
	return string(data)
}

func getrustAuditInternal(fileName string) string {
	returnValue := `{ "error" : "Unknown" }`
	r, err := os.Open(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf(`{ "error": "path error:%v" }`, fileName)
		} else {
			returnValue = fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
		}
		return returnValue
	}
	defer r.Close()

	pkgList, err := rustaudit.GetDependencyInfo(r)
	if err != nil {
		return fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
	}
	data, _ := json.Marshal(pkgList)
	return string(data)
}

func getGoBuildInfoInternal(fileName string) string {
	returnValue := `{ "error" : "Unknown" }`
	bi, err := buildinfo.ReadFile(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf(`{ "error": "path error:%v" }`, fileName)
		} else {
			returnValue = fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
		}
		return returnValue
	}
	data, _ := json.Marshal(bi)
	return string(data)
}

func getGoMod(fileName string) string {
	returnValue := `{ "error" : "Unknown" }`
	f, err := os.Open(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf(`{ "error": "path error:%v" }`, fileName)
		} else {
			returnValue = fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
		}
		return returnValue
	}
	defer f.Close()

	goModData, err := io.ReadAll(f)
	if err != nil {
		return fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
	}
	modFileParsed, err := modfile.Parse("go.mod", goModData, nil)
	if err != nil {
		return fmt.Sprintf(`{ "error": "%s: %v"}`, fileName, err)
	}
	data, _ := json.Marshal(modFileParsed)
	return string(data)
}

var _ = sqlite.Driver{}
