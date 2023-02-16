import os
import yaml


class DistroMetadata:
    def __init__(
            self, name: str = "rMaker Distro", version: str = "1.0", codename: str = "Cardinal Cobalt",
            base: str = "none", identifier: str = "rmakerdistro", url: str = "https://example.com"):
        self.name = name
        self.version = version
        self.codename = codename
        self.identifier = identifier
        self.url = url
        self.base_distro = base
        self._os_release = ""
        self.reset_os_release()

    def get_os_release(self) -> dict:
        return self._os_release

    def set_os_release(self, os_release: dict):
        self._os_release = os_release

    def modify_os_release(self, key: str, value: str):
        self._os_release[key] = value

    def generate_os_release(self) -> dict:
        os_release = ""
        for key, value in self._os_release.items():
            os_release += f"{key}={value}"
        return os_release

    def reset_os_release(self):
        self._os_release = {
            "NAME": self.name,
            "VERSION": f"{self.version} ({self.codename})",
            "ID": self.identifier,
            "ID_LIKE": self.base_distro,
            "VERSION_ID": self.version,
            "PRETTY_NAME": f"{self.name} {self.version} ({self.codename})",
            "ANSI_COLOR": "1;32",
            "HOME_URL": self.url,
            "SUPPORT_URL": self.url,
            "BUG_REPORT_URL": self.url
        }

    @classmethod
    def new_from_yaml(cls, yaml_file: str):
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f.read())
            try:
                metadata_dict = data["Metadata"]
                metadata = cls(
                    name=metadata_dict["name"],
                    version=metadata_dict["version"],
                    codename=metadata_dict["codename"],
                    base=metadata_dict["base"],
                    identifier=metadata_dict["identifier"],
                    url=metadata_dict["url"]
                )
                for key, value in metadata_dict["os_release"].items():
                    metadata.modify_os_release(key, value)
            except KeyError:
                print("Unable to parse metadata from yaml file. Using default values.")
                metadata = cls()
            return metadata

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict())

    def to_dict(self) -> dict:
        dictionary = {
            "Metadata": {
                "name": self.name,
                "version": self.version,
                "codename": self.codename,
                "base": self.base_distro,
                "identifier": self.identifier,
                "url": self.url,
                "os_release": self._os_release
            }
        }
        return dictionary


class DistroPackages:
    def __init__(self, packages: list = [], removed_packages: list = []):
        self._packages = packages  # Packages to be installed
        self._removed_packages = removed_packages  # Packages to remove on top of the base distro's packages

    def get_packages(self) -> list:
        return self._packages

    def set_packages(self, packages: list):
        self._packages = packages

    def add_package(self, package):
        self._packages.append(package)

    def get_removed_packages(self) -> list:
        return self._removed_packages

    def set_removed_packages(self, packages: list):
        self._removed_packages = packages

    def remove_package(self, package: str, remove_globally: bool = True):
        if package in self._packages:
            self._packages.remove(package)
        if remove_globally:
            self.removed_packages.append(package)

    @classmethod
    def new_from_yaml(cls, yaml_file: str):
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f.read())
            try:
                packages_dict = data["Packages"]
            except KeyError:
                print("Unable to parse packages from yaml file. Using default values.")
                packages_dict = {"added": [], "removed": []}
            return cls(packages_dict["added"], packages_dict["removed"])

    def to_yaml(self):
        return yaml.dump(self.to_dict())

    def to_dict(self) -> dict:
        return {"Packages": {"added": self._packages, "removed": self._removed_packages}}


class CustomPackage:
    def __init__(self, name: str, directory: str):
        self.name = ""
        self.directory = ""

        if type(self) is CustomPackage:
            raise NotImplementedError("CustomPackage is an abstract class and cannot be instantiated.")

    def Generate(self):
        NotImplementedError("CustomPackage.build() is not implemented.")


class PackageBuilder:
    def __init__(self, packages: list = []):
        self._packages = packages

    def add_package(self, package: CustomPackage):
        self._packages.append(package)

    def remove_package(self, package: CustomPackage):
        if package in self._packages:
            self._packages.remove(package)

    def get_packages(self):
        return self._packages

    def build_packages(self, output_directory: str):
        raise NotImplementedError("This method must be implemented by a child class.")


class IsoBuilder:
    def __init__(self, distro_metadata: DistroMetadata = None, distro_packages: DistroPackages = None):
        self._distro_metadata = distro_metadata
        self._distro_packages = distro_packages
        self._gsettings = {}
        self._package_builder = None
        self._project_directory = os.getcwd()

        # Abstract class
        if self.__class__ is IsoBuilder:
            raise NotImplementedError("This class is an abstract class and cannot be instantiated.")

    def set_project_directory(self, project_directory: str):
        self._project_directory = project_directory

    def get_project_directory(self) -> str:
        return self._project_directory

    def set_distro_metadata(self, distro_metadata: DistroMetadata):
        self._distro_metadata = distro_metadata

    def get_distro_metadata(self) -> DistroMetadata:
        return self._distro_metadata

    def set_distro_packages(self, distro_packages: DistroPackages):
        self._distro_packages = distro_packages

    def get_distro_packages(self) -> DistroPackages:
        return self._distro_packages

    def set_gsettings(self, gsettings: dict):
        self._gsettings = gsettings

    def get_gsettings(self) -> dict:
        return self._gsettings

    def add_gsetting(self, key: str, value: str):
        self._gsettings[key] = value

    def add_custom_package(self, package: CustomPackage):
        self._package_builder.add_package(package)

    def remove_custom_package(self, package: CustomPackage):
        self._package_builder.remove_package(package)

    def build_custom_packages(self, output_directory: str):
        self._package_builder.build_packages(output_directory)

    def build_iso(self):
        raise NotImplementedError("This method must be implemented by a child class.")

    @classmethod
    def new_from_yaml(cls, yaml_file: str):
        raise NotImplementedError("This method must be implemented by a child class.")
