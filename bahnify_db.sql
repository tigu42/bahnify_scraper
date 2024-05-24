-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: bahnify
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `delay`
--

DROP TABLE IF EXISTS `delay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delay` (
  `train` varchar(100) NOT NULL,
  `current_arrival` datetime DEFAULT NULL,
  `current_departure` datetime DEFAULT NULL,
  `current_origin` varchar(900) NOT NULL,
  `current_destination` varchar(900) NOT NULL,
  `info` varchar(150) NOT NULL,
  `status` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `current_last_station` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `delay_un` (`train`),
  KEY `delay_FK_1` (`status`),
  CONSTRAINT `delay_FK` FOREIGN KEY (`train`) REFERENCES `train` (`id`),
  CONSTRAINT `delay_FK_1` FOREIGN KEY (`status`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2119705 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delay`
--

LOCK TABLES `delay` WRITE;
/*!40000 ALTER TABLE `delay` DISABLE KEYS */;
/*!40000 ALTER TABLE `delay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directions`
--

DROP TABLE IF EXISTS `directions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directions` (
  `id` int(11) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directions`
--

LOCK TABLES `directions` WRITE;
/*!40000 ALTER TABLE `directions` DISABLE KEYS */;
INSERT INTO `directions` VALUES (1,'arriving'),(2,'departing'),(3,'arriving_departing');
/*!40000 ALTER TABLE `directions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operators`
--

DROP TABLE IF EXISTS `operators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operators` (
  `operator` varchar(5) NOT NULL,
  `travel_type` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`operator`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operators`
--

LOCK TABLES `operators` WRITE;
/*!40000 ALTER TABLE `operators` DISABLE KEYS */;
INSERT INTO `operators` VALUES ('ag','regional','agilis'),('AKN','unknown','unknown'),('ALX','regional','Alex'),('AS','unknown','unknown'),('BRB','regional','Bayerische Regiobahn'),('Bus','regional','Bus'),('CB','unknown','unknown'),('D','long_distance','Durchgangszug'),('DBK','Sonderzug','Dampfzug '),('EC','long_distance','EuroCity'),('ECE','long_distance','EuroCityExpress'),('EN','long_distance','EuroNight'),('ENO','regional','Enno'),('erx','regional','erixx'),('ES','long_distance','EuroStar'),('EST','long_distance','EuroStar International'),('FEX','regional','Flughafen-Express'),('FLX','long_distance','FlixTrain'),('HBX','regional','Harz-Berlin-Express'),('HLB','regional','Hessische Landesbahn'),('IC','long_distance','Intercity'),('ICE','long_distance','Intercity Express'),('IR','long_distance','Interregio'),('IRE','regional','InterregioExpress'),('ME','regional','metronom'),('MEX','regional','Metropolexpress'),('MSM','unknown','unknown'),('N','regional','Regio-S-Bahn'),('NBE','regional','Nordbahn Eisenbahngesellschaft'),('NJ','long_distance','Night Jet'),('NWB','regional','NordWestBahn'),('OPB','regional','OberPfalzBahn'),('OPX','regional','OberPfalzExpress'),('R','regional','Regionalzug (Ö)'),('RB','regional','Regionalbahn'),('RE','regional','RegionalExpress'),('REX','regional','Regionalexpress (Ö)'),('RJ','long_distance','RailJet'),('RJX','long_distance','RailJetExpress'),('RRB','regional','RheinRuhrBahn'),('RT','regional','RegioTram'),('S','regional','S-Bahn'),('SAB','regional','Schwäbische Alb-Bahn'),('SBB','regional','Schweizer Bundesbahn'),('STN','regional','Regionalverkehre Start Deutschland GmbH'),('SVG','regional','unknown'),('SWE','regional','Südwestdeutsche Landesverkehrs-GmbH'),('TGV','long_distance','TGV'),('TL','regional','Trilex'),('TLX','regional','TrilexExpress'),('TRI','unknown','unknown'),('UEX','unknown','unknown'),('VBG','unknown','unknown'),('VIA','regional','Vias'),('WB','long_distance','WESTbahn'),('WEG','regional','Württembergische Eisenbahn-Gesellschaft mbH'),('WFB','regional','Westfalenbahn');
/*!40000 ALTER TABLE `operators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `eva` int(10) unsigned NOT NULL,
  `description` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  PRIMARY KEY (`eva`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='A collection of train stations';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `status_id` int(10) unsigned NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'ok'),(2,'canceled');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train`
--

DROP TABLE IF EXISTS `train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `train` (
  `id` varchar(100) NOT NULL,
  `type` varchar(10) NOT NULL,
  `alias` varchar(10) NOT NULL,
  `train_number` varchar(10) NOT NULL,
  `platform` varchar(15) NOT NULL,
  `station` int(10) unsigned NOT NULL,
  `scheduled_departure` datetime DEFAULT NULL,
  `scheduled_arrival` datetime DEFAULT NULL,
  `scheduled_origin` varchar(800) NOT NULL,
  `scheduled_destination` varchar(800) NOT NULL,
  `direction` int(11) NOT NULL,
  `last_station` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `train_FK` (`station`),
  KEY `train_FK_1` (`direction`),
  CONSTRAINT `train_FK` FOREIGN KEY (`station`) REFERENCES `station` (`eva`),
  CONSTRAINT `train_FK_1` FOREIGN KEY (`direction`) REFERENCES `directions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train`
--

LOCK TABLES `train` WRITE;
/*!40000 ALTER TABLE `train` DISABLE KEYS */;
/*!40000 ALTER TABLE `train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'bahnify'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-22 15:39:50
