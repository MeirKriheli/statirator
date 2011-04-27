from statirator import config
import unittest

class TestSiteConfig(unittest.TestCase):

    def test_default_config(self):
        """Validate site's default configuration"""

        cfg = config.SiteConfig()

        self.assertFalse(cfg.is_multilingual)
        self.assertEqual(cfg.lanauges, 'en')
        self.assertEqual(cfg.multilinugal_scheme, 'path')

        self.assertEqual(cfg.base_domain, 'example.com')
        self.assertEqual(cfg.site_name, 'Example')
