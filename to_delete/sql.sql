CREATE TABLE `rooms`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` varchar(2000)   NOT NULL,
  `description` longtext   NULL,
  `content` longtext   NULL,
  `floor` int(255) NULL DEFAULT NULL,
  `image` int(11) NOT NULL COMMENT '{\"relation\":\"hasOne\",\"table\":\"images\"}',
  `images` varchar(2000)   NULL DEFAULT NULL COMMENT '{\"relation\":\"belongsToMany\",\"table\":\"images\",\"middle_table\":\"room_image\"}',



  `video` int(11) NOT NULL COMMENT '{\"relation\":\"hasOne\",\"table\":\"videos\"}',
  `flash` int(11) NULL DEFAULT NULL COMMENT '{\"relation\":\"hasOne\",\"table\":\"flashes\"}',

  `locked-days` varchar(2000)   NULL DEFAULT NULL,
  `inactive-days` varchar(2000)   NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '{\"relation\":\"hasMany\",\"table\":\"room_prices\",\"field\":\"room\"}',
  `hotel` int(255) NULL DEFAULT NULL COMMENT '{\"relation\":\"belongsTo\",\"table\":\"hotels\"}',
  `available` int(255) NULL DEFAULT NULL,
  `created_at` timestamp(0) NULL DEFAULT NULL,
  `updated_at` timestamp(0) NULL DEFAULT NULL,
)
