/*
 Navicat Premium Data Transfer

 Source Server         : 10.0.1.14
 Source Server Type    : MySQL
 Source Server Version : 50173
 Source Host           : 10.0.1.14
 Source Database       : metadata

 Target Server Type    : MySQL
 Target Server Version : 50173
 File Encoding         : utf-8

 Date: 07/26/2016 10:46:42 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `Department`
-- ----------------------------
DROP TABLE IF EXISTS `Department`;
CREATE TABLE `Department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `parentId` int(11) NOT NULL,
  `code` varchar(20) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Department`
-- ----------------------------
BEGIN;
INSERT INTO `Department` VALUES ('1', '数据中心', '0', '12', 'A'), ('2', '数据部', '1', '104', 'A'), ('4', '客服部', '1', '103', 'A'), ('8', '办公室', '1', '101', 'A'), ('11', '业务中心', '1', '102', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `Department_copy`
-- ----------------------------
DROP TABLE IF EXISTS `Department_copy`;
CREATE TABLE `Department_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `parentId` int(11) NOT NULL,
  `code` varchar(20) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Department_copy`
-- ----------------------------
BEGIN;
INSERT INTO `Department_copy` VALUES ('1', '数据中心', '0', '12', 'A'), ('2', '数据部', '1', '104', 'A'), ('4', '客服部', '1', '103', 'A'), ('8', '办公室', '1', '101', 'A'), ('11', '业务中心', '1', '102', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `Dictionary`
-- ----------------------------
DROP TABLE IF EXISTS `Dictionary`;
CREATE TABLE `Dictionary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(40) DEFAULT NULL,
  `key` varchar(100) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  `sortIndex` int(11) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Dictionary`
-- ----------------------------
BEGIN;
INSERT INTO `Dictionary` VALUES ('1', '初始化网站设置', '质检系统', '网站名称', 'A', null, null), ('2', '初始化网站设置', 'localhost:8090', '网站地址', 'A', null, null), ('3', '初始化网站设置', '172.31.117.194', '归集端地址', 'A', null, null), ('4', '初始化网站设置', '172.31.117.194', '调听地址', 'A', null, null), ('5', '初始化定时任务设置', 'cn.com.centrin.basic.service.impl', '系统数据清理', 'A', null, null), ('6', '初始化定时任务设置', 'cn.com.centrin.basic.service.impl', '系统数据清理2', 'A', null, null), ('7', '初始化定时任务定时器设置', '0 0/20 * * *', '默认设置', 'A', null, null), ('8', '初始化定时任务定时器设置', '0 0/20 * * *', '系统数据清理', 'A', null, null), ('10', '语音枚举-通话类型', 'A', '呼入', 'A', null, null), ('9', '定时任务定时器设置', '0 0/20 * * *', '系统数据清理2', 'A', null, null), ('11', '语音枚举-通话类型', 'B', '呼出', 'A', null, null), ('12', '语音枚举-满意度', 'A', '满意', 'A', null, null), ('13', '语音枚举-满意度', 'B', '一般', 'A', null, null), ('14', '语音枚举-满意度', 'C', '不满意', 'A', null, null), ('15', '语音枚举-情绪', '1', '愉快', 'A', null, null), ('16', '语音枚举-情绪', '2', '烦躁', 'A', null, null), ('17', '语音枚举-情绪', '3', '不满', 'A', null, null), ('18', '质检-关联质检周期', '7', '周', 'A', null, null), ('19', '质检-关联质检周期', '10', '旬', 'A', null, null), ('20', '质检-关联质检周期', '15', '半月', 'A', null, null), ('21', '质检-关联质检周期', '30', '月', 'A', null, null), ('22', '质检-关联质检类型', 'forward', '向前', 'A', null, null), ('23', '质检-关联质检类型', 'backward', '向后', 'A', null, null), ('24', '质检-关联质检关联字段', 'phoneID', '电话号', 'A', null, null), ('25', '质检-关联质检关联字段', 'accountNo', '用户卡号', 'A', null, null), ('26', '质检-关联质检关联字段', 'busiNo', '业务单号', 'A', null, null), ('27', '定时任务设置2', '111', '定时数据清理', 'A', '11', null), ('28', '初始化Redis地址', 'dictionaryManagerImpl', '数据字典', 'A', '1', null), ('29', '初始化Redis地址', 'departmentManagerImpl', '组织机构', 'A', '2', null), ('30', '初始化Redis地址', 'businessTypeManagerImpl', '业务类型', 'A', '3', null), ('31', '初始化数据库原始表', 'VoiceTemp_Init', '语音临时数据表', 'A', '1', ''), ('32', '初始化数据库原始表', 'Voice_Init', '语音表', 'A', '2', '10'), ('33', '初始化数据库原始表', 'VoiceInfo_Init', '语音业务数据表', 'A', '3', '10'), ('34', '初始化数据库原始表', 'VoiceRep_Init', '话务员表', 'A', '4', null), ('35', '初始化数据库原始表', 'VoiceAccount_Init', '客户表', 'A', '5', null), ('36', '初始化数据库原始表', 'VoiceAccountBusi_Init', '客户业务表', 'A', '6', null), ('37', '初始化数据库', 'quality', '数据库名', 'A', '1', null), ('38', '初始化数据库表', 'VoiceTemp_Res', '语音临时数据表', 'A', '1', null), ('39', '初始化数据库表', 'Voice_Res', '语音表', 'A', '2', null), ('40', '初始化数据库表', 'VoiceInfo_Res', '语音业务数据表', 'A', '3', null), ('41', '初始化数据库表', 'VoiceRep_Res', '话务员表', 'A', '4', null), ('42', '初始化数据库表', 'VoiceAccount_Res', '客户表', 'A', '5', null), ('43', '初始化数据库表', 'VoiceAccountBusi_Res', '客户业务表', 'A', '6', null), ('44', '初始化数据库原始表', 'QualityFile_Init', '质检文件结果表', 'A', '7', '1'), ('45', '初始化Redis地址', 'keywordTypeManagerImpl', '关键词分类', 'A', '4', null), ('46', '初始化Redis地址', 'qualityTypeManagerImpl', '质检规则分类', 'A', '5', null), ('47', '初始化Redis地址', 'voiceCallReasonAManagerImpl', '一级原因', 'A', '6', null), ('48', '初始化Redis地址', 'voiceCallReasonBManagerImpl', '二级原因', 'A', '7', null), ('49', '语音', '1', '语音', 'A', '1', null), ('50', '语音2', '2', '语音', 'A', '1', null), ('51', '初始化Redis地址', 'keywordManagerImpl', '关键词', 'A', '8', 'List');
COMMIT;

-- ----------------------------
--  Table structure for `KeyWord`
-- ----------------------------
DROP TABLE IF EXISTS `KeyWord`;
CREATE TABLE `KeyWord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywordTypeId` int(11) DEFAULT NULL,
  `keyword` varchar(40) DEFAULT NULL COMMENT '关键词',
  `synonym` varchar(100) DEFAULT NULL COMMENT '同义词',
  `active` varchar(1) DEFAULT NULL COMMENT '是否有效',
  `createTime` varchar(20) DEFAULT NULL COMMENT '创建日期',
  `createUser` varchar(20) DEFAULT NULL COMMENT '创建人',
  `usableTime` varchar(20) DEFAULT NULL,
  `forbiddenTime` varchar(20) DEFAULT NULL,
  `lastModifyTime` varchar(20) DEFAULT NULL COMMENT '最近修改日期',
  `lastModifyUser` varchar(20) DEFAULT NULL COMMENT '最近修改人',
  `remark` varchar(200) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `KeyWord`
-- ----------------------------
BEGIN;
INSERT INTO `KeyWord` VALUES ('22', '6', '您好', null, 'A', '2016-04-05 17:18:31', '1', '2016-04-05 17:18:31', null, '2016-04-05 17:18:31', '1', 'delete from Keyword'), ('23', '7', '您好么', null, 'A', '2016-04-05 17:19:20', '1', '2016-04-05 17:19:20', null, '2016-04-05 17:19:20', '1', null), ('24', '6', 'ninh', null, 'A', '2016-04-05 17:21:59', '1', '2016-04-05 17:21:59', null, '2016-04-05 17:21:59', '1', null), ('25', '6', 'ninh', null, 'A', '2016-04-05 17:24:04', '1', '2016-04-05 17:24:04', null, '2016-04-05 17:24:04', '1', null), ('26', '6', 'nind', null, 'A', '2016-04-05 17:24:26', '1', '2016-04-05 17:24:26', null, '2016-04-05 17:24:26', '1', null), ('27', '8', '文明用语', null, 'A', '2016-04-06 11:25:49', '1', '2016-04-06 11:25:49', null, '2016-04-06 11:25:49', '1', '文明用语文明用语文明用语');
COMMIT;

-- ----------------------------
--  Table structure for `MetaDetail`
-- ----------------------------
DROP TABLE IF EXISTS `MetaDetail`;
CREATE TABLE `MetaDetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meta_id` varchar(40) DEFAULT NULL,
  `serial` int(11) DEFAULT NULL,
  `field` varchar(50) DEFAULT NULL,
  `field_name` varchar(50) DEFAULT NULL,
  `field_type` varchar(20) DEFAULT NULL,
  `primary_key` varchar(1) DEFAULT NULL,
  `field_info` varchar(1000) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `used` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaDetail`
-- ----------------------------
BEGIN;
INSERT INTO `MetaDetail` VALUES ('3', 'baidugps', '1', 'ID', 'ID', 'String', 'A', null, '1', 'A'), ('4', 'baidugps', '2', 'time', '时间', 'String', 'A', null, '1', 'A'), ('5', 'baidugps', '3', 'longitude', '经度', 'String', 'A', null, '1', 'A'), ('6', 'baidugps', '4', 'latitude', '纬度', 'String', 'A', null, '1', 'A'), ('7', 'baidugps', '5', 'speed', '速度', 'String', 'A', null, '1', 'A'), ('8', 'baidugps', '6', 'direction', '方向', 'String', 'A', null, '1', 'A'), ('9', 'NASDAQ_daily_prices', '1', 'exchange', 'exchange', 'String', 'B', null, '1', 'A'), ('10', 'NASDAQ_daily_prices', '2', 'stock_symbol', 'stock_symbol', 'String', 'B', null, '1', 'A'), ('11', 'NASDAQ_daily_prices', '3', 'date', 'date', 'String', 'B', null, '1', 'A'), ('12', 'NASDAQ_daily_prices', '4', 'stock_price_open', 'stock_price_open', 'String', 'B', null, '1', 'A'), ('13', 'NASDAQ_daily_prices', '5', 'stock_price_high', 'stock_price_high', 'String', 'B', null, '1', 'A'), ('14', 'NASDAQ_daily_prices', '6', 'stock_price_low', 'stock_price_low', 'String', 'B', null, '1', 'A'), ('15', 'NASDAQ_daily_prices', '7', 'stock_price_close', 'stock_price_close', 'String', 'B', null, '1', 'A'), ('16', 'NASDAQ_daily_prices', '8', 'stock_volume', 'stock_volume', 'String', 'B', null, '1', 'A'), ('17', 'NASDAQ_daily_prices', '9', 'stock_price_adj_clos', 'stock_price_adj_clos', 'String', 'B', null, '1', 'A'), ('18', 'baidugps', '1', 'id', 'id', 'int', 'A', null, '1', 'A'), ('19', 'person', '1', 'id', 'id', 'int', 'A', null, '1', 'A'), ('20', 'person', '2', 'name', 'name', 'String', 'B', null, '1', 'A'), ('21', 'person', '3', 'age', 'age', 'int', 'B', null, '1', 'A'), ('22', 'person', '4', 'sex', 'sex', 'String', 'B', null, '1', 'A'), ('23', 'person', '5', 'area', 'area', 'String', 'B', null, '1', 'A'), ('24', 'person', '6', 'nation', 'nation', 'String', 'B', null, '1', 'A'), ('25', 'person', '7', 'edu', 'edu', 'String', 'B', null, '1', 'A'), ('26', 'person', '8', 'job', 'job', 'String', 'B', null, '1', 'A'), ('27', 'person', '9', 'marital', 'marital', 'String', 'B', null, '1', 'A'), ('28', 'person', '10', 'type', 'type', 'String', 'B', null, '1', 'A'), ('29', 'person', '11', 'created', 'cteated', 'int', 'B', null, '1', 'A'), ('30', 'person', '12', 'modified', 'modified', 'int', 'B', null, '1', 'A'), ('31', 'person', '13', 'phone_number', 'phone_number', 'String', 'B', null, '1', 'A'), ('32', 'person', '14', 'astro', 'astro', 'String', 'B', null, '1', 'A'), ('33', 'person', '15', 'email', 'email', 'String', 'B', null, '1', 'A'), ('34', 'person', '16', 'imei', 'imei', 'String', 'B', null, '1', 'A'), ('35', 'person', '17', 'on_internet_time', 'on_internet_time', 'String', 'B', null, '1', 'A'), ('36', 'person', '18', 'qq', 'qq', 'String', 'B', null, '1', 'A'), ('37', 'person', '19', 'taobao', 'taobao', 'String', 'B', null, '1', 'A'), ('38', 'person', '20', 'jd', 'jd', 'String', 'B', null, '1', 'A'), ('39', 'person', '21', 'weibo', 'weibo', 'String', 'B', null, '1', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `MetaInfo`
-- ----------------------------
DROP TABLE IF EXISTS `MetaInfo`;
CREATE TABLE `MetaInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meta_id` varchar(40) NOT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `table_cname` varchar(100) DEFAULT NULL,
  `file_location` varchar(200) DEFAULT NULL,
  `mutifile` varchar(1) DEFAULT NULL,
  `file_type` varchar(50) DEFAULT NULL,
  `file_split` varchar(10) DEFAULT NULL,
  `quantity` varchar(20) DEFAULT NULL,
  `data_number` varchar(20) DEFAULT NULL,
  `response` varchar(20) DEFAULT NULL,
  `data_desc` varchar(1000) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `used` varchar(1) DEFAULT NULL,
  `changeinfo` varchar(1000) DEFAULT NULL,
  `metatype_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `metatype_id` (`metatype_id`),
  CONSTRAINT `metainfo_ibfk_1` FOREIGN KEY (`metatype_id`) REFERENCES `MetaType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaInfo`
-- ----------------------------
BEGIN;
INSERT INTO `MetaInfo` VALUES ('5', 'baidugps', 'baidugps', null, '/user/root/smartv/hive/baidugps', 'A', 'csv', ',', '10G', '5000', null, null, '1', 'A', null, '5'), ('6', 'NASDAQ_daily_prices', 'NASDAQ_daily_prices', null, '/user/root/smartv/hive/NASDAQ_daily_prices', 'A', 'csv', ',', 'T', '100000', null, 'NASDAQ数据', null, 'A', null, '5'), ('7', 'person', 'person', null, '/user/root/smartv/hive/person', 'A', 'txt', ',', 'GB', '10000', null, null, null, 'A', null, '5');
COMMIT;

-- ----------------------------
--  Table structure for `MetaManager`
-- ----------------------------
DROP TABLE IF EXISTS `MetaManager`;
CREATE TABLE `MetaManager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meta_id` varchar(40) NOT NULL,
  `lifecycle` int(11) DEFAULT NULL,
  `updatecycle` int(11) DEFAULT NULL,
  `share` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaManager`
-- ----------------------------
BEGIN;
INSERT INTO `MetaManager` VALUES ('1', 'baidugps', '365', '1', 'B'), ('25', 'NASDAQ_daily_prices', '720', '2', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `MetaMapping`
-- ----------------------------
DROP TABLE IF EXISTS `MetaMapping`;
CREATE TABLE `MetaMapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meta_id` varchar(40) NOT NULL,
  `meta_source` varchar(40) DEFAULT NULL,
  `etl_engine` varchar(40) DEFAULT NULL,
  `etl_config` varchar(200) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `used` varchar(1) DEFAULT NULL,
  `changeinfo` varchar(1000) DEFAULT NULL,
  `cronExpression` varchar(150) DEFAULT NULL COMMENT '定时表达式',
  `jobGroup` varchar(100) DEFAULT NULL COMMENT '定时任务组',
  `jobName` varchar(100) DEFAULT NULL COMMENT '定时任务名称',
  `isSync` varchar(10) DEFAULT NULL COMMENT '同步任务：1，是，0,否',
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaMapping`
-- ----------------------------
BEGIN;
INSERT INTO `MetaMapping` VALUES ('7', 'baidugps', '文件', 'kettle', '/opt/test-data/jobgps.sh', '1', '1', '1', '0 */10 * * * ?', 'testGroup', 'testJob2', '1', null), ('8', 'NASDAQ_daily_prices', '文件', 'kettle', '/opt/test-data/job1.sh', '1', '1', '1', '0 */15 * * * ?', 'testGroup', 'testJob1', '1', null), ('9', 'person', 'mysql', 'sqoop', '/opt/test-data/sqoop_person.sh', '1', 'A', null, '0 */20 * * * ?', 'sqoop', 'person-trans', 'A', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `MetaRelation`
-- ----------------------------
DROP TABLE IF EXISTS `MetaRelation`;
CREATE TABLE `MetaRelation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meta_id` varchar(40) DEFAULT NULL,
  `field` varchar(50) DEFAULT NULL,
  `meta2_id` varchar(40) DEFAULT NULL,
  `field2` varchar(50) DEFAULT NULL,
  `rules` varchar(200) DEFAULT NULL,
  `mapping` varchar(1) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `used` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaRelation`
-- ----------------------------
BEGIN;
INSERT INTO `MetaRelation` VALUES ('1', 'baidugps', '12', '12', '12', '12', '1', '12', '1'), ('3', 'persion', '11', '11', '11', '11', '1', '11', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `MetaType`
-- ----------------------------
DROP TABLE IF EXISTS `MetaType`;
CREATE TABLE `MetaType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `parentId` int(11) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `MetaType`
-- ----------------------------
BEGIN;
INSERT INTO `MetaType` VALUES ('5', '互联网数据', '001', '0', 'A');
COMMIT;

-- ----------------------------
--  Table structure for `SecurityModule`
-- ----------------------------
DROP TABLE IF EXISTS `SecurityModule`;
CREATE TABLE `SecurityModule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentId` int(11) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `showName` varchar(20) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `sortIndex` int(11) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  `isMenu` varchar(1) DEFAULT NULL,
  `isOpenNew` varchar(1) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=132 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
--  Records of `SecurityModule`
-- ----------------------------
BEGIN;
INSERT INTO `SecurityModule` VALUES ('2', '0', '02', '权限管理', '权限管理', '', '8', 'A', 'A', 'B', null), ('3', '0', '03', '系统配置', '系统配置', '', '9', 'A', 'A', 'B', null), ('21', '2', '0201', '授权管理', '授权管理', '/securityModule/index', '4', 'A', 'A', 'B', null), ('22', '2', '0202', '角色管理', '角色管理', '/securityRole/index', '2', 'A', 'A', 'B', null), ('23', '2', '0203', '用户管理', '用户管理', '/securityUser/index', '1', 'A', 'A', 'B', null), ('31', '2', '0204', '组织机构管理', '组织机构管理', '/basicDepartment/index', '1', 'A', 'A', 'B', null), ('33', '3', '0303', '业务类型', '业务类型管理', '/basicBusinessType/index', '3', 'B', 'A', 'B', null), ('36', '3', '0306', '系统数据字典管理', '系统数据字典管理', '/basicDictionary/index', '6', 'B', 'A', 'B', null), ('101', '21', '020101', '菜单列表展示', '菜单列表展示', '/securityModule/list', '1', 'A', 'B', null, null), ('102', '21', '020102', '菜单添加', '菜单添加', '/securityModule/save', '2', 'A', 'B', null, null), ('103', '21', '020103', '菜单编辑', '菜单编辑', '/securityModule/update', '3', 'A', 'B', null, null), ('104', '21', '020104', '菜单删除', '菜单删除', '/securityModule/delete', '4', 'A', 'B', null, null), ('105', '21', '020105', '菜单批量删除', '菜单批量删除', '/securityModule/batchDelete', '5', 'A', 'B', null, null), ('106', '21', '020106', '菜单启用', '菜单启用', '/securityModule/active', '6', 'A', 'B', null, null), ('108', '21', '020108', '菜单禁用', '菜单禁用', '/securityModule/noActive', '8', 'A', 'B', null, null), ('107', '21', '020107', '菜单批量启用', '菜单批量启用', '/securityModule/batchActive', '7', 'A', 'B', null, null), ('109', '21', '020109', '菜单批量禁用', '菜单批量禁用', '/securityModule/batchNoActive', '9', 'A', 'B', null, null), ('111', '3', '0308', '元数据分类管理', '元数据分类管理', '/basicMetaType/index', '8', 'A', 'A', 'B', null), ('112', '3', '0309', '元数据管理', '元数据管理', '/basicMetaInfo/index', '9', 'A', 'A', 'B', null), ('113', '3', '0310', '管理模型', '管理模型', '/basicMetaManager/index', '10', 'A', 'A', 'B', null), ('114', '3', '0311', '元数据结构', '元数据结构', '/basicMetaDetail/index', '11', 'A', 'A', 'B', null), ('115', '3', '0312', '映射关系', '映射关系', '/basicMetaMapping/index', '12', 'A', 'A', 'B', null), ('116', '3', '0313', '关联关系', '关联关系', '/basicMetaRelation/index', '13', 'A', 'A', 'B', null), ('117', '0', '04', '归集任务管理', '归集任务管理', null, '10', 'A', 'A', 'B', null), ('118', '117', '0401', '计划中任务', '计划中任务', '/schedule/jobIndex', '1', 'A', 'A', 'B', null), ('119', '117', '0402', '运行中任务', '运行中任务', '/schedule/executingJobIndex', '2', 'A', 'A', 'B', null);
COMMIT;

-- ----------------------------
--  Table structure for `SecurityRole`
-- ----------------------------
DROP TABLE IF EXISTS `SecurityRole`;
CREATE TABLE `SecurityRole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `showName` varchar(20) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `SecurityRole`
-- ----------------------------
BEGIN;
INSERT INTO `SecurityRole` VALUES ('1', '管理员', '管理员', 'A', '管理员管理员管理员管理员管理员管理员管理员管理员管理员管理员'), ('2', '质检管理员', '质检管理员', 'A', null), ('3', '质检员', '质检员', 'A', null), ('4', '质检检查员', '质检检查员', 'A', null);
COMMIT;

-- ----------------------------
--  Table structure for `SecurityRoleModule`
-- ----------------------------
DROP TABLE IF EXISTS `SecurityRoleModule`;
CREATE TABLE `SecurityRoleModule` (
  `roleId` int(11) NOT NULL,
  `moduleId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`moduleId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=FIXED;

-- ----------------------------
--  Records of `SecurityRoleModule`
-- ----------------------------
BEGIN;
INSERT INTO `SecurityRoleModule` VALUES ('1', '2'), ('1', '3'), ('1', '21'), ('1', '22'), ('1', '23'), ('1', '31'), ('1', '101'), ('1', '102'), ('1', '103'), ('1', '104'), ('1', '105'), ('1', '106'), ('1', '107'), ('1', '108'), ('1', '109'), ('1', '111'), ('1', '112'), ('1', '117'), ('1', '118'), ('1', '119'), ('16', '2'), ('16', '21'), ('16', '22'), ('16', '23'), ('16', '101'), ('16', '102'), ('16', '103'), ('16', '104'), ('16', '105'), ('16', '106'), ('16', '107'), ('16', '108'), ('16', '109'), ('17', '2'), ('17', '21'), ('17', '22'), ('17', '23'), ('17', '101'), ('17', '102'), ('17', '103'), ('17', '104'), ('17', '105'), ('17', '106'), ('17', '107'), ('17', '108'), ('17', '109');
COMMIT;

-- ----------------------------
--  Table structure for `SecurityUser`
-- ----------------------------
DROP TABLE IF EXISTS `SecurityUser`;
CREATE TABLE `SecurityUser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departmentId` int(11) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `realName` varchar(40) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `identity` varchar(10) DEFAULT NULL,
  `active` varchar(1) DEFAULT NULL,
  `loginFailed` int(2) DEFAULT NULL,
  `createTime` varchar(20) DEFAULT NULL,
  `createUser` int(11) DEFAULT NULL,
  `lastModifyTime` varchar(20) DEFAULT NULL,
  `lastModifyUser` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `SecurityUser`
-- ----------------------------
BEGIN;
INSERT INTO `SecurityUser` VALUES ('1', '1', 'admin', 'admin', '管理员', '256996305635895008EEEF1C3EF11BBF', 'A', 'A', '0', null, null, null, null), ('2', '1', 'user1', 'user1', 'user1', '9E1FF7CC4D136DA23C70A1A96D15E39A', 'A', 'A', null, '2016-03-10 13:46:21', '1', '2016-03-10 13:46:21', '1'), ('3', '1', '用户2', '用户2', '用户2', '23FCBE3032F2D7BD2429983908F13C3F', 'A', 'B', null, null, null, null, null), ('4', '1', '用户2', '用户2', '用户2', null, 'A', 'B', null, null, null, null, null), ('5', '1', '用户2', '用户2', '用户2', null, 'A', 'A', null, null, null, null, null), ('6', '1', '用户3', '用户3', '用户3', null, 'A', 'A', null, null, null, null, null), ('7', '1', '用户4', '用户4', '用户4', null, 'A', 'B', null, null, null, null, null), ('12', '2', 'gyx', 'ss', 'sss', 'D1EAA57FCD4A5742B6843A56E9525A97', 'A', 'A', null, '2016-05-19 15:15:40', '1', '2016-05-19 15:15:40', '1'), ('11', '1', '用户7', '用户7', '用户7', '48C601430236CD6766DC89968B5AF834', 'A', 'A', null, '2016-03-10 14:19:08', '1', '2016-03-10 14:19:08', '1');
COMMIT;

-- ----------------------------
--  Table structure for `SecurityUserRole`
-- ----------------------------
DROP TABLE IF EXISTS `SecurityUserRole`;
CREATE TABLE `SecurityUserRole` (
  `userId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`roleId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `SecurityUserRole`
-- ----------------------------
BEGIN;
INSERT INTO `SecurityUserRole` VALUES ('1', '1'), ('10', '1'), ('10', '4'), ('10', '8'), ('11', '1'), ('11', '4'), ('11', '8'), ('12', '1'), ('12', '2');
COMMIT;

-- ----------------------------
--  Function structure for `getDepartmentParentId`
-- ----------------------------
DROP FUNCTION IF EXISTS `getDepartmentParentId`;
delimiter ;;
CREATE DEFINER=`root`@`10.0.5.%` FUNCTION `getDepartmentParentId`(departmentId integer,intervalStr CHAR) RETURNS varchar(1000) CHARSET utf8
BEGIN
     DECLARE rtnStr VARCHAR(1000);
     DECLARE l_name VARCHAR(100);
     DECLARE l_parentId INT;
     SET l_parentId=1;
     WHILE l_parentId >0 DO
SET l_parentId=0;
          select parentId,name from Department where id=departmentId into l_parentId,l_name;
          IF (LENGTH(rtnStr)>0) THEN
               SET rtnStr=CONCAT(intervalStr,l_parentId,intervalStr,rtnStr);
          ELSE
               SET rtnStr=CONCAT(intervalStr,l_parentId,intervalStr);
          END IF;
                    SET departmentId=l_parentId;
     END WHILE;
     RETURN rtnStr;
END
 ;;
delimiter ;

-- ----------------------------
--  Function structure for `getDepartmentParentName`
-- ----------------------------
DROP FUNCTION IF EXISTS `getDepartmentParentName`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `getDepartmentParentName`(departmentId integer,intervalStr CHAR) RETURNS varchar(1000) CHARSET utf8
BEGIN
     DECLARE rtnStr VARCHAR(1000);
     DECLARE l_name VARCHAR(100);
     DECLARE l_parentId INT;
     SET l_parentId=1;
     WHILE l_parentId >0 DO 
SET l_parentId=0;
          select parentId,name from Department where id=departmentId into l_parentId,l_name;
          IF (LENGTH(rtnStr)>0) THEN
               SET rtnStr=CONCAT(l_name,intervalStr,rtnStr);
          ELSE
               SET rtnStr=l_name;
          END IF;
				 SET departmentId=l_parentId;
     END WHILE;
     RETURN rtnStr;
END
 ;;
delimiter ;

