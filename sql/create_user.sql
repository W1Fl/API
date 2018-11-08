CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usr` varchar(16) NOT NULL,
  `password` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usr` (`usr`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8
