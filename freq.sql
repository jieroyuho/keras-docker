USE conndb;
CREATE TABLE IF NOT EXISTS `conn` (
  `timestamp` text COLLATE utf8_unicode_ci,
  `sip` text COLLATE utf8_unicode_ci,
  `sport` text COLLATE utf8_unicode_ci,
  `dip` text COLLATE utf8_unicode_ci,
  `dport` text COLLATE utf8_unicode_ci,
  `byte` text COLLATE utf8_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

