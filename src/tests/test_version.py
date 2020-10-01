from unittest import TestCase, mock

from tagversion.version import Version


class VersionTestCase(TestCase):
    def test_bump_major(self, *mocks):
        """Ensure major is bumped"""

        version = Version.parse("0.0.0")
        version.bump(bump_major=True)

        self.assertEquals(
            "1.0.0",
            str(version),
        )

    def test_bump_minor(self, *mocks):
        """Ensure minor is bumped"""

        version = Version.parse("0.0.0")
        version.bump(bump_minor=True)

        self.assertEquals(
            "0.1.0",
            str(version),
        )

    def test_bump_patch(self, *mocks):
        """Ensure patch is bumped"""

        version = Version.parse("0.0.0")
        version.bump(bump_patch=True)

        self.assertEquals(
            "0.0.1",
            str(version),
        )

    def test_bump_new_prerelease(self, *mocks):
        """Ensure prerelease is added"""

        version = Version.parse("0.0.1")
        version.bump(bump_prerelease=True)

        self.assertEquals(
            "0.0.1rc1",
            str(version),
        )

    def test_bump_prerelease(self, *mocks):
        """Ensure prerelease is bumped"""

        version = Version.parse("0.0.1rc1")
        version.bump(bump_prerelease=True)

        self.assertEquals(
            "0.0.1rc2",
            str(version),
        )

    def test_bump_to_prerelease(self, *mocks):
        """Ensure patch and prerelease is set"""

        version = Version.parse("0.1.27-16-g5befeb2-feature--skip-prefix-rows")
        version.bump(bump_patch=True, bump_prerelease=True)

        self.assertEquals(
            "0.1.28rc1",
            str(version),
        )

    def test_bump_prerelease_to_stable(self, *mocks):
        """Ensure prerelease is dropped"""

        version = Version.parse("0.0.1rc1")
        version.bump()

        self.assertEquals(
            "0.0.1",
            str(version),
        )

    def test_is_prerelease(self, *mocks):
        """Ensure prereleases are properly detected"""

        version = Version.parse("0.0.1rc16")

        self.assertEquals(
            True,
            version.is_prerelease,
        )

    def test_is_rc(self, *mocks):
        """Ensure rc part of the tag flags rc"""

        version = Version.parse("0.0.1rc16")

        self.assertEquals(
            True,
            version.is_rc,
        )

    def test_is_unreleased(self, *mocks):
        """Ensure unreleased versions are properly detected"""

        version = Version.parse("66cf7c2-HEAD")

        self.assertEquals(
            False,
            version.is_prerelease,
        )

        self.assertEquals(
            True,
            version.is_unreleased,
        )

    def test_parse_git(self, *mocks):
        """parsing a version that's not an exact tag"""

        version = Version.parse("TestModule/0.0.1-16-g5befeb2")

        self.assertEquals(
            "16-g5befeb2",
            version.prerelease,
        )

        self.assertEquals(
            Version(
                major=0,
                minor=0,
                patch=1,
                prefix="TestModule/",
                prereleasedash="-",
                prerelease="16-g5befeb2",
            ),
            version,
        )

    def test_parse_rc(self, *mocks):
        """Ensure rc part of the tag ends up in the prerelease attr"""

        version = Version.parse("0.0.1rc16")

        self.assertEquals(
            "rc16",
            version.prerelease,
        )

    def test_parse_semver(self, *mocks):
        """Ensure a basic semver is parsed"""

        version = Version.parse("0.0.1")

        self.assertEquals(Version(major=0, minor=0, patch=1), version)

    def test_parse_semver_with_prefix(self, *mocks):
        """Ensure a basic semver with a prefix is parsed"""

        version = Version.parse("TestModule/0.0.1")

        self.assertEquals(
            Version(major=0, minor=0, patch=1, prefix="TestModule/"), version
        )

        self.assertEquals("TestModule/0.0.1", str(version))

    def test_parse_untagged(self, *mocks):
        """Ensure an untagged version can be parsed"""

        version_s = "66cf7c2-HEAD"
        version = Version.parse(version_s)

        self.assertEquals(
            Version(major=None, minor=None, patch=None, prerelease=version_s),
            version,
        )

        self.assertEquals(version_s, str(version))
