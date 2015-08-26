-- Adminer 4.2.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP DATABASE IF EXISTS `ionstreamer`;
CREATE DATABASE `ionstreamer` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `ionstreamer`;

DROP TABLE IF EXISTS `keyword`;
CREATE TABLE `keyword` (
  `keyword` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(16) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'inactive',
  `processing` tinyint(4) NOT NULL DEFAULT '0',
  `since_id` bigint(20) NOT NULL DEFAULT '0',
  `max_id` bigint(20) NOT NULL DEFAULT '0',
  `last_modified` timestamp NOT NULL,
  PRIMARY KEY (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- DROP TABLE IF EXISTS `token`;
-- CREATE TABLE `token` (
--   `name` varchar(32) NOT NULL,
--   `last_used` datetime NOT NULL,
--   `CONSUMER_KEY` varchar(32) NOT NULL,
--   `CONSUMER_SECRET` varchar(64) NOT NULL,
--   `OAUTH_TOKEN` varchar(64) NOT NULL,
--   `OAUTH_TOKEN_SECRET` varchar(64) NOT NULL,
--   PRIMARY KEY (`CONSUMER_KEY`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- TRUNCATE `token`;
-- INSERT INTO `token` (`name`, `last_used`, `CONSUMER_KEY`, `CONSUMER_SECRET`, `OAUTH_TOKEN`, `OAUTH_TOKEN_SECRET`) VALUES
-- ('ionstreamer-alt-1',	'2015-07-28 11:46:28',	'A2HealPlVlNSjw3rRvnD8QRV7',	'2OlELoONajWemE5GFyCWaQJn2pSuT9wmtkNa3sxRVnOC646Tmd',	'165650047-zFVIH8Vk9Td1iwBa4JNzPBJhdQGiTTEvG64UnxGa',	'gDqe5PPBiBC5s8GOIH0ZQ7I4AsDxUyw2S2aP9BHyMExYp'),
-- ('ionstreamer',	'2015-07-28 11:46:31',	'fnLxpCb6OsyiQtlsRJOJqsjYv',	'vwV5CqozRk7dYlHKrQxcHpedFFkR8w5gQX0Wg0NC0Wr5AQcvgW',	'165650047-HT1d922Xru54UUvtArQawP2h99vYLecnqR01vAtK',	'bhsIEb3cKMyuIT9v2IYFsnIpl7SEOpO8NUe3SdObWCE6e'),
-- ('ionstreamer-past',	'2015-07-28 11:46:21',	'IG5oRi05KtnMJ5waQMJAhAC1X',	'0PGIjKti23UxrpQRw4EtExBD18MWl9AuxwmXShdKOhGN2dGrOr',	'165650047-1r3WzaRmGh0cPnNoiIhhVuhS1DhjwQJAzZWPhlg4',	'HDDnA7ZGfBRJRCXIS77W9B7jBZn5WPnG0ejHaDLwD2Ul3'),
-- ('ionstreamer-alt-2',	'2015-07-28 11:32:49',	'mlmsUwE0Im7xoAR40rdjmbd80',	'BfDzWjCR9OuzUFGDqC5FxU0xsHF1JSD95rpJcD6qNOyjX4NeO4',	'165650047-5BAvI1wh1BZxhutSeQwjkyt5tUQ2nT3uxNqA6P7u',	'54fELPoxh4o0yNb6artdR8nJsQsOsvhvyrLMPi8xQyIwc'),
-- ('ionstreamer-alt-3',	'2015-07-28 07:05:58',	'phDMeAths0X5NytM5pl13sj0a',	'DLpYTv2dDCvWsCWxKzKbiqGu4Ygcnq456w9TX6mEJVaHSGEcWg',	'165650047-RNbqgodWgqxWsUOcz95TEmXhMTi4tNxT3kglwEzv',	'PmniFgaq0t5LQ1Zy13616McqIwuxGiFGWsrx29D8SKKda');

-- -- 2015-07-29 03:37:03
