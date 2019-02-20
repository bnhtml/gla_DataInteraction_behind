-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Aacl`
--

# DROP TABLE IF EXISTS `Aacl`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Aacl` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `serviceName` varchar(80) NOT NULL,
#   `name` varchar(80) NOT NULL,
#   `whitelist` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Acontrols`
--

# DROP TABLE IF EXISTS `Acontrols`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Acontrols` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(80) NOT NULL,
#   `consumer_id` varchar(80) NOT NULL,
#   `day` varchar(80) NOT NULL,
#   `serviceName` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Agroup`
--

# DROP TABLE IF EXISTS `Agroup`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Agroup` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `group` varchar(80) NOT NULL,
#   `username` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Aservice`
--

# DROP TABLE IF EXISTS `Aservice`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Aservice` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `serviceName` varchar(80) NOT NULL,
#   `hosts` varchar(80) NOT NULL,
#   `uris` varchar(80) NOT NULL,
#   `upstream_url` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `serviceName` (`serviceName`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Auser`
--

# DROP TABLE IF EXISTS `Auser`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Auser` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `username` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `users_username_983a7b636a27e55_uniq` (`username`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `departlog`
--

DROP TABLE IF EXISTS `departlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detartTask` varchar(100) NOT NULL,
  `detartObject` varchar(100) NOT NULL,
  `detartUser` varchar(100) NOT NULL,
  `detartAirtime` varchar(100) NOT NULL,
  `detartEndtime` varchar(100) NOT NULL,
  `superStatus` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `commonlog`
--

DROP TABLE IF EXISTS `commonlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commonlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detartTask` varchar(100) NOT NULL,
  `detartObject` varchar(100) NOT NULL,
  `detartUser` varchar(100) NOT NULL,
  `detartAirtime` varchar(100) NOT NULL,
  `detartEndtime` varchar(100) NOT NULL,
  `superStatus` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `savetable`
--

DROP TABLE IF EXISTS `savetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `savetable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tableName` varchar(80) ,
  `us_tableName` varchar(80) ,
  `is_delete` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;




--
-- Table structure for table `add_field`
--

DROP TABLE IF EXISTS `add_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `add_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fieldName` varchar(80) ,
  `fieldDesc` varchar(80) ,
  `fieldType` varchar(80) ,
  `is_delete` varchar(80) ,
  `tableKey_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `add_field_3c5e8884` (`tableKey_id`),
  CONSTRAINT `add_field_tableKey_id_56938975a3f6cea9_fk_savetable_id` FOREIGN KEY (`tableKey_id`) REFERENCES `savetable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `dbList`
--

DROP TABLE IF EXISTS `dbList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dbName` varchar(300) NOT NULL,
  `dbSql` varchar(4000) NOT NULL,
  `dbIP` varchar(300) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `fileList`
--

DROP TABLE IF EXISTS `fileList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(300) NOT NULL,
  `fileIP` varchar(300) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `interfaceList`
--

DROP TABLE IF EXISTS `interfaceList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaceList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interfaceName` varchar(300) NOT NULL,
  `interfaceIP` varchar(300) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `messageList`
--

DROP TABLE IF EXISTS `messageList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messageList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `messageName` varchar(300) NOT NULL,
  `messageIP` varchar(300) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;




--
-- Table structure for table `Uacl`
--


DROP TABLE IF EXISTS `Uacl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Uacl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serviceName` varchar(80) NOT NULL,
  `aclName` varchar(80) NOT NULL,
  `whitelist` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ucontrols`
--

DROP TABLE IF EXISTS `Ucontrols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ucontrols` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `controlsName` varchar(80) NOT NULL,
  `userName` varchar(80) NOT NULL,
  `consumer_id` varchar(80) NOT NULL,
  `serviceName` varchar(80) NOT NULL,
  `day` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ugroup`
--

DROP TABLE IF EXISTS `Ugroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ugroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(80) NOT NULL,
  `userName` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Uservice`
--

DROP TABLE IF EXISTS `Uservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Uservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serviceName` varchar(80) NOT NULL,
  `hosts` varchar(80) NOT NULL,
  `uris` varchar(80) NOT NULL,
  `client_type` varchar(80) NOT NULL,
  `upstream_url` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `serviceName` (`serviceName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

# --
# -- Table structure for table `Uuser`
# --
#
# DROP TABLE IF EXISTS `Uuser`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `Uuser` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `userName` varchar(80) NOT NULL,
#   `apiKey` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `users_username_983a7b636a27e55_uniq` (`username`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `AdminFirst`
--

DROP TABLE IF EXISTS `AdminFirst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AdminFirst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department` varchar(100) NOT NULL,
  `chinese_abb` varchar(80) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `AdminSecond`
--

DROP TABLE IF EXISTS `AdminSecond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AdminSecond` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `industry` varchar(100) NOT NULL,
  `chinese_abb` varchar(80) NOT NULL,
  `is_delete` int(11) NOT NULL,
  `first_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AdminSecond_first_id_21a3528323c49927_fk_AdminFirst_id` (`first_id`),
  CONSTRAINT `AdminSecond_first_id_21a3528323c49927_fk_AdminFirst_id` FOREIGN KEY (`first_id`) REFERENCES `AdminFirst` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `AdminThird`
--

DROP TABLE IF EXISTS `AdminThird`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AdminThird` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `species` varchar(100) NOT NULL,
  `chinese_abb` varchar(80) NOT NULL,
  `is_delete` int(11) NOT NULL,
  `first_id` int(11) NOT NULL,
  `second_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AdminThird_first_id_ad84673fff1c2cf_fk_AdminFirst_id` (`first_id`),
  KEY `AdminThird_second_id_7add8f0e66c7ec8_fk_AdminSecond_id` (`second_id`),
  CONSTRAINT `AdminThird_first_id_ad84673fff1c2cf_fk_AdminFirst_id` FOREIGN KEY (`first_id`) REFERENCES `AdminFirst` (`id`),
  CONSTRAINT `AdminThird_second_id_7add8f0e66c7ec8_fk_AdminSecond_id` FOREIGN KEY (`second_id`) REFERENCES `AdminSecond` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `fileName`
--

DROP TABLE IF EXISTS `fileName`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileName` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fileParams`
--

DROP TABLE IF EXISTS `fileParams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileParams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(200) NOT NULL,
  `file_desc` varchar(200) NOT NULL,
  `file_type` varchar(200) NOT NULL,
  `filename_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fileParams_filename_id_id_732b12d6c48994e3_fk_fileName_id` (`filename_id_id`),
  CONSTRAINT `fileParams_filename_id_id_732b12d6c48994e3_fk_fileName_id` FOREIGN KEY (`filename_id_id`) REFERENCES `fileName` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `interfaceName`
--

DROP TABLE IF EXISTS `interfaceName`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaceName` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interface_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `interfaceParams`
--

DROP TABLE IF EXISTS `interfaceParams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaceParams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interface_name` varchar(200) NOT NULL,
  `interface_desc` varchar(200) NOT NULL,
  `interface_type` varchar(200) NOT NULL,
  `interface_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interfacePa_interface_id_id_73bdcd9ddfffff28_fk_interfaceName_id` (`interface_id_id`),
  CONSTRAINT `interfacePa_interface_id_id_73bdcd9ddfffff28_fk_interfaceName_id` FOREIGN KEY (`interface_id_id`) REFERENCES `interfaceName` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messageName`
--

DROP TABLE IF EXISTS `messageName`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messageName` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messageParams`
--

DROP TABLE IF EXISTS `messageParams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messageParams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_name` varchar(200) NOT NULL,
  `message_desc` varchar(200) NOT NULL,
  `message_type` varchar(200) NOT NULL,
  `message_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `messageParams_message_id_id_7db90679338043d1_fk_messageName_id` (`message_id_id`),
  CONSTRAINT `messageParams_message_id_id_7db90679338043d1_fk_messageName_id` FOREIGN KEY (`message_id_id`) REFERENCES `messageName` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


# --
# -- Table structure for table `BasicInter`
# --
#
# DROP TABLE IF EXISTS `BasicInter`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `BasicInter` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
# #   `department` varchar(100) NOT NULL,
#   `hosts` varchar(80) NOT NULL,
#   `is_delete` int(11) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# /*!40101 SET character_set_client = @saved_cs_client */;

-- --
-- -- Table structure for table `serverdict`
-- --
--
-- DROP TABLE IF EXISTS `serverdict`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `serverdict` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `name` varchar(300) NOT NULL,
--   `top_class` varchar(300) NOT NULL,
--   `type` varchar(200) NOT NULL,
--   `server_name` longtext NOT NULL,
--   `data_name` longtext NOT NULL,
--   `is_delete` int(11) NOT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- /*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-27 13:40:10


