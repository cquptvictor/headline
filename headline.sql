/*
 Navicat Premium Data Transfer

 Source Server         : my-aliyun
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : 47.107.129.3:3306
 Source Schema         : headline

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 22/11/2019 11:09:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` datetime(0) NULL,
  `author` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pic` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `category` char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `comment_num` int(11) NOT NULL DEFAULT 0,
  `read_num` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  FULLTEXT INDEX `1`(`title`)
) ENGINE = InnoDB AUTO_INCREMENT = 1968 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for authentication
-- ----------------------------
DROP TABLE IF EXISTS `authentication`;
CREATE TABLE `authentication`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `auth_code` int(11) NOT NULL,
  `time` float(32, 0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for collection
-- ----------------------------
DROP TABLE IF EXISTS `collection`;
CREATE TABLE `collection`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(4) NOT NULL,
  `article_id` int(8) NOT NULL,
  `time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `u`(`article_id`, `uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `article_id` int(8) NOT NULL,
  `uid` int(4) NOT NULL,
  `content` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `like_num` int(8) NOT NULL DEFAULT 0,
  `read_num` int(8) NULL DEFAULT 0,
  `time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for fans
-- ----------------------------
DROP TABLE IF EXISTS `fans`;
CREATE TABLE `fans`  (
  `uid` int(11) NOT NULL,
  `fans_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for follow
-- ----------------------------
DROP TABLE IF EXISTS `follow`;
CREATE TABLE `follow`  (
  `uid` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for reply
-- ----------------------------
DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply`  (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `cid` int(4) NULL DEFAULT NULL COMMENT '关联comment表',
  `from_id` int(4) NOT NULL,
  `to_id` int(11) NOT NULL,
  `to_name` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `like_num` int(11) NOT NULL DEFAULT 0,
  `time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `reply_id` int(11) NOT NULL,
  `type` int(255) NOT NULL COMMENT '0代表回复评论',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 77 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ucollection
-- ----------------------------
DROP TABLE IF EXISTS `ucollection`;
CREATE TABLE `ucollection`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(4) NOT NULL,
  `article_id` int(8) NOT NULL,
  `time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `u`(`article_id`, `uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1111',
  `email` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` char(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fans_num` int(11) NOT NULL DEFAULT 0,
  `follow_num` int(11) NOT NULL DEFAULT 0,
  `pic` char(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'http://127.0.0.1:5050/static/img/default.jpg',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_headline
-- ----------------------------
DROP TABLE IF EXISTS `user_headline`;
CREATE TABLE `user_headline`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(4) NOT NULL,
  `content` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `read_num` int(11) NOT NULL DEFAULT 0,
  `like_num` int(11) NOT NULL DEFAULT 0,
  `time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `pic` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for zan
-- ----------------------------
DROP TABLE IF EXISTS `zan`;
CREATE TABLE `zan`  (
  `uid` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`uid`, `article_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Procedure structure for auth
-- ----------------------------
DROP PROCEDURE IF EXISTS `auth`;
delimiter ;;
CREATE DEFINER=`root`@`%` PROCEDURE `auth`()
BEGIN
	#Routine body goes here...
delete from authentication  WHERE DATE_SUB(CURRENT_TIMESTAMP,INTERVAL 300 Second)>authentication.time;
END
;;
delimiter ;

-- ----------------------------
-- Event structure for delete_authCode
-- ----------------------------
DROP EVENT IF EXISTS `delete_authCode`;
delimiter ;;
CREATE DEFINER = `root`@`%` EVENT `delete_authCode`
ON SCHEDULE
EVERY '24' HOUR STARTS '2019-02-25 08:45:56'
ON COMPLETION PRESERVE
DO delete from authentication where DATE_SUB(CURRENT_TIMESTAMP,INTERVAL 400 second)
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
