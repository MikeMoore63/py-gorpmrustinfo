from setuptools import Extension, setup

if __name__ == "__main__":
    setup(
        build_golang={"root": "github.com/MikeMoore63/pygorpmrustinfo"},
        ext_modules=[
            Extension(
                "pygorpmrustinfo._pygorpmrustinfo",
                ["src/pygorpmrustinfo/pygorpmrustinfo.go"],
            )
        ],
    )
