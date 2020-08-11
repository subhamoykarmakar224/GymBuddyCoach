CREATE DATABASE  IF NOT EXISTS `gymms` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `gymms`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: gymms
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gymadmin`
--

DROP TABLE IF EXISTS `gymadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gymadmin` (
  `gymId` varchar(100) NOT NULL,
  `memberrole` varchar(100) DEFAULT NULL,
  `gymName` varchar(100) DEFAULT NULL,
  `adminName` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `validity` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `passwd` text,
  `loginstatus` int DEFAULT NULL,
  PRIMARY KEY (`gymId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gymadmin`
--

LOCK TABLES `gymadmin` WRITE;
/*!40000 ALTER TABLE `gymadmin` DISABLE KEYS */;
INSERT INTO `gymadmin` VALUES ('BodyShapersGym-2932','admin','Body Shapers Gym','Modi','+919876543210','31-09-2020','mods','7110eda4d09e062aa5e4a390b0a572ac0d2c0220',1);
/*!40000 ALTER TABLE `gymadmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `localaction`
--

DROP TABLE IF EXISTS `localaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localaction` (
  `actiontime` datetime DEFAULT NULL,
  `module` varchar(100) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localaction`
--

LOCK TABLES `localaction` WRITE;
/*!40000 ALTER TABLE `localaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `localaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `notifId` varchar(100) NOT NULL,
  `studentId` varchar(100) DEFAULT NULL,
  `dateTime` varchar(100) DEFAULT NULL,
  `level` varchar(10) DEFAULT NULL,
  `msg` text,
  PRIMARY KEY (`notifId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwareflags`
--

DROP TABLE IF EXISTS `softwareflags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwareflags` (
  `flagname` varchar(100) DEFAULT NULL,
  `status` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwareflags`
--

LOCK TABLES `softwareflags` WRITE;
/*!40000 ALTER TABLE `softwareflags` DISABLE KEYS */;
INSERT INTO `softwareflags` VALUES ('firstinstallstudent',1);
/*!40000 ALTER TABLE `softwareflags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `SID` varchar(100) NOT NULL,
  `allotedtime` varchar(200) DEFAULT NULL,
  `membershipvalidity` varchar(200) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `studentage` varchar(100) DEFAULT NULL,
  `studentname` varchar(100) DEFAULT NULL,
  `regstatus` varchar(100) DEFAULT NULL,
  `dueamount` varchar(100) DEFAULT '0',
  PRIMARY KEY (`SID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('ID-2932-0f23a6df','03:00 PM to 04:00 PM','2020-09-10','+919432743720','1991-10-16','Subhamoy Karmakar','1','0');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-11 17:10:50
