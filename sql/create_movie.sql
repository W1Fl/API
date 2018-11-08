CREATE TABLE `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `片名` char(100) NOT NULL,
  `简介` text,
  `海报` char(150) DEFAULT NULL,
  `导演` char(150) DEFAULT NULL,
  `编剧` char(150) DEFAULT NULL,
  `主演` text,
  `类型` char(50) DEFAULT NULL,
  `制片国家` char(200) DEFAULT NULL,
  `语言` char(200) DEFAULT NULL,
  `上映日期` char(200) DEFAULT NULL,
  `片长` char(100) DEFAULT NULL,
  `又名` char(200) DEFAULT NULL,
  `评分` float DEFAULT NULL,
  `观看地址` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `movies_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8
