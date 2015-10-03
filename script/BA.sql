CREATE TABLE `page_content` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL,
  `content` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `cached_url` (
  `url` varchar(256)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;