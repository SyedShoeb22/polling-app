/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: lxp.c3aku00wug16.us-east-1.rds.amazonaws.com    Database: performance_schema
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `CURRENT_CONNECTIONS` bigint NOT NULL,
  `TOTAL_CONNECTIONS` bigint NOT NULL,
  `MAX_SESSION_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_SESSION_TOTAL_MEMORY` bigint unsigned NOT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `binary_log_transaction_compression_stats`
--

DROP TABLE IF EXISTS `binary_log_transaction_compression_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `binary_log_transaction_compression_stats` (
  `LOG_TYPE` enum('BINARY','RELAY') NOT NULL COMMENT 'The log type to which the transactions were written.',
  `COMPRESSION_TYPE` varchar(64) NOT NULL COMMENT 'The transaction compression algorithm used.',
  `TRANSACTION_COUNTER` bigint unsigned NOT NULL COMMENT 'Number of transactions written to the log',
  `COMPRESSED_BYTES_COUNTER` bigint unsigned NOT NULL COMMENT 'The total number of bytes compressed.',
  `UNCOMPRESSED_BYTES_COUNTER` bigint unsigned NOT NULL COMMENT 'The total number of bytes uncompressed.',
  `COMPRESSION_PERCENTAGE` smallint NOT NULL COMMENT 'The compression ratio as a percentage.',
  `FIRST_TRANSACTION_ID` text COMMENT 'The first transaction written.',
  `FIRST_TRANSACTION_COMPRESSED_BYTES` bigint unsigned NOT NULL COMMENT 'First transaction written compressed bytes.',
  `FIRST_TRANSACTION_UNCOMPRESSED_BYTES` bigint unsigned NOT NULL COMMENT 'First transaction written uncompressed bytes.',
  `FIRST_TRANSACTION_TIMESTAMP` timestamp(6) NULL DEFAULT NULL COMMENT 'When the first transaction was written.',
  `LAST_TRANSACTION_ID` text COMMENT 'The last transaction written.',
  `LAST_TRANSACTION_COMPRESSED_BYTES` bigint unsigned NOT NULL COMMENT 'Last transaction written compressed bytes.',
  `LAST_TRANSACTION_UNCOMPRESSED_BYTES` bigint unsigned NOT NULL COMMENT 'Last transaction written uncompressed bytes.',
  `LAST_TRANSACTION_TIMESTAMP` timestamp(6) NULL DEFAULT NULL COMMENT 'When the last transaction was written.'
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `binary_log_transaction_compression_stats`
--

LOCK TABLES `binary_log_transaction_compression_stats` WRITE;
/*!40000 ALTER TABLE `binary_log_transaction_compression_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `binary_log_transaction_compression_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cond_instances`
--

DROP TABLE IF EXISTS `cond_instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cond_instances` (
  `NAME` varchar(128) NOT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  PRIMARY KEY (`OBJECT_INSTANCE_BEGIN`),
  KEY `NAME` (`NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cond_instances`
--

LOCK TABLES `cond_instances` WRITE;
/*!40000 ALTER TABLE `cond_instances` DISABLE KEYS */;
/*!40000 ALTER TABLE `cond_instances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_lock_waits`
--

DROP TABLE IF EXISTS `data_lock_waits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_lock_waits` (
  `ENGINE` varchar(32) NOT NULL,
  `REQUESTING_ENGINE_LOCK_ID` varchar(128) NOT NULL,
  `REQUESTING_ENGINE_TRANSACTION_ID` bigint unsigned DEFAULT NULL,
  `REQUESTING_THREAD_ID` bigint unsigned DEFAULT NULL,
  `REQUESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `REQUESTING_OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `BLOCKING_ENGINE_LOCK_ID` varchar(128) NOT NULL,
  `BLOCKING_ENGINE_TRANSACTION_ID` bigint unsigned DEFAULT NULL,
  `BLOCKING_THREAD_ID` bigint unsigned DEFAULT NULL,
  `BLOCKING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `BLOCKING_OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  PRIMARY KEY (`REQUESTING_ENGINE_LOCK_ID`,`BLOCKING_ENGINE_LOCK_ID`,`ENGINE`),
  KEY `REQUESTING_ENGINE_LOCK_ID` (`REQUESTING_ENGINE_LOCK_ID`,`ENGINE`),
  KEY `BLOCKING_ENGINE_LOCK_ID` (`BLOCKING_ENGINE_LOCK_ID`,`ENGINE`),
  KEY `REQUESTING_ENGINE_TRANSACTION_ID` (`REQUESTING_ENGINE_TRANSACTION_ID`,`ENGINE`),
  KEY `BLOCKING_ENGINE_TRANSACTION_ID` (`BLOCKING_ENGINE_TRANSACTION_ID`,`ENGINE`),
  KEY `REQUESTING_THREAD_ID` (`REQUESTING_THREAD_ID`,`REQUESTING_EVENT_ID`),
  KEY `BLOCKING_THREAD_ID` (`BLOCKING_THREAD_ID`,`BLOCKING_EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_lock_waits`
--

LOCK TABLES `data_lock_waits` WRITE;
/*!40000 ALTER TABLE `data_lock_waits` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_lock_waits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_locks`
--

DROP TABLE IF EXISTS `data_locks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_locks` (
  `ENGINE` varchar(32) NOT NULL,
  `ENGINE_LOCK_ID` varchar(128) NOT NULL,
  `ENGINE_TRANSACTION_ID` bigint unsigned DEFAULT NULL,
  `THREAD_ID` bigint unsigned DEFAULT NULL,
  `EVENT_ID` bigint unsigned DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(64) DEFAULT NULL,
  `PARTITION_NAME` varchar(64) DEFAULT NULL,
  `SUBPARTITION_NAME` varchar(64) DEFAULT NULL,
  `INDEX_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `LOCK_TYPE` varchar(32) NOT NULL,
  `LOCK_MODE` varchar(32) NOT NULL,
  `LOCK_STATUS` varchar(32) NOT NULL,
  `LOCK_DATA` varchar(8192) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ENGINE_LOCK_ID`,`ENGINE`),
  KEY `ENGINE_TRANSACTION_ID` (`ENGINE_TRANSACTION_ID`,`ENGINE`),
  KEY `THREAD_ID` (`THREAD_ID`,`EVENT_ID`),
  KEY `OBJECT_SCHEMA` (`OBJECT_SCHEMA`,`OBJECT_NAME`,`PARTITION_NAME`,`SUBPARTITION_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_locks`
--

LOCK TABLES `data_locks` WRITE;
/*!40000 ALTER TABLE `data_locks` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_locks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `error_log`
--

DROP TABLE IF EXISTS `error_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `error_log` (
  `LOGGED` timestamp(6) NOT NULL,
  `THREAD_ID` bigint unsigned DEFAULT NULL,
  `PRIO` enum('System','Error','Warning','Note') NOT NULL,
  `ERROR_CODE` varchar(10) DEFAULT NULL,
  `SUBSYSTEM` varchar(7) DEFAULT NULL,
  `DATA` text NOT NULL,
  PRIMARY KEY (`LOGGED`),
  KEY `THREAD_ID` (`THREAD_ID`),
  KEY `PRIO` (`PRIO`),
  KEY `ERROR_CODE` (`ERROR_CODE`),
  KEY `SUBSYSTEM` (`SUBSYSTEM`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error_log`
--

LOCK TABLES `error_log` WRITE;
/*!40000 ALTER TABLE `error_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `error_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_errors_summary_by_account_by_error`
--

DROP TABLE IF EXISTS `events_errors_summary_by_account_by_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_errors_summary_by_account_by_error` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `ERROR_NUMBER` int DEFAULT NULL,
  `ERROR_NAME` varchar(64) DEFAULT NULL,
  `SQL_STATE` varchar(5) DEFAULT NULL,
  `SUM_ERROR_RAISED` bigint unsigned NOT NULL,
  `SUM_ERROR_HANDLED` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_SEEN` timestamp NULL DEFAULT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`,`ERROR_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_errors_summary_by_account_by_error`
--

LOCK TABLES `events_errors_summary_by_account_by_error` WRITE;
/*!40000 ALTER TABLE `events_errors_summary_by_account_by_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_errors_summary_by_account_by_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_errors_summary_by_host_by_error`
--

DROP TABLE IF EXISTS `events_errors_summary_by_host_by_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_errors_summary_by_host_by_error` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `ERROR_NUMBER` int DEFAULT NULL,
  `ERROR_NAME` varchar(64) DEFAULT NULL,
  `SQL_STATE` varchar(5) DEFAULT NULL,
  `SUM_ERROR_RAISED` bigint unsigned NOT NULL,
  `SUM_ERROR_HANDLED` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_SEEN` timestamp NULL DEFAULT NULL,
  UNIQUE KEY `HOST` (`HOST`,`ERROR_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_errors_summary_by_host_by_error`
--

LOCK TABLES `events_errors_summary_by_host_by_error` WRITE;
/*!40000 ALTER TABLE `events_errors_summary_by_host_by_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_errors_summary_by_host_by_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_errors_summary_by_thread_by_error`
--

DROP TABLE IF EXISTS `events_errors_summary_by_thread_by_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_errors_summary_by_thread_by_error` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `ERROR_NUMBER` int DEFAULT NULL,
  `ERROR_NAME` varchar(64) DEFAULT NULL,
  `SQL_STATE` varchar(5) DEFAULT NULL,
  `SUM_ERROR_RAISED` bigint unsigned NOT NULL,
  `SUM_ERROR_HANDLED` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_SEEN` timestamp NULL DEFAULT NULL,
  UNIQUE KEY `THREAD_ID` (`THREAD_ID`,`ERROR_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_errors_summary_by_thread_by_error`
--

LOCK TABLES `events_errors_summary_by_thread_by_error` WRITE;
/*!40000 ALTER TABLE `events_errors_summary_by_thread_by_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_errors_summary_by_thread_by_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_errors_summary_by_user_by_error`
--

DROP TABLE IF EXISTS `events_errors_summary_by_user_by_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_errors_summary_by_user_by_error` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `ERROR_NUMBER` int DEFAULT NULL,
  `ERROR_NAME` varchar(64) DEFAULT NULL,
  `SQL_STATE` varchar(5) DEFAULT NULL,
  `SUM_ERROR_RAISED` bigint unsigned NOT NULL,
  `SUM_ERROR_HANDLED` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_SEEN` timestamp NULL DEFAULT NULL,
  UNIQUE KEY `USER` (`USER`,`ERROR_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_errors_summary_by_user_by_error`
--

LOCK TABLES `events_errors_summary_by_user_by_error` WRITE;
/*!40000 ALTER TABLE `events_errors_summary_by_user_by_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_errors_summary_by_user_by_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_errors_summary_global_by_error`
--

DROP TABLE IF EXISTS `events_errors_summary_global_by_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_errors_summary_global_by_error` (
  `ERROR_NUMBER` int DEFAULT NULL,
  `ERROR_NAME` varchar(64) DEFAULT NULL,
  `SQL_STATE` varchar(5) DEFAULT NULL,
  `SUM_ERROR_RAISED` bigint unsigned NOT NULL,
  `SUM_ERROR_HANDLED` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_SEEN` timestamp NULL DEFAULT NULL,
  UNIQUE KEY `ERROR_NUMBER` (`ERROR_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_errors_summary_global_by_error`
--

LOCK TABLES `events_errors_summary_global_by_error` WRITE;
/*!40000 ALTER TABLE `events_errors_summary_global_by_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_errors_summary_global_by_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_current`
--

DROP TABLE IF EXISTS `events_stages_current`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_current` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `WORK_COMPLETED` bigint unsigned DEFAULT NULL,
  `WORK_ESTIMATED` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_current`
--

LOCK TABLES `events_stages_current` WRITE;
/*!40000 ALTER TABLE `events_stages_current` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_current` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_history`
--

DROP TABLE IF EXISTS `events_stages_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_history` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `WORK_COMPLETED` bigint unsigned DEFAULT NULL,
  `WORK_ESTIMATED` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_history`
--

LOCK TABLES `events_stages_history` WRITE;
/*!40000 ALTER TABLE `events_stages_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_history_long`
--

DROP TABLE IF EXISTS `events_stages_history_long`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_history_long` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `WORK_COMPLETED` bigint unsigned DEFAULT NULL,
  `WORK_ESTIMATED` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_history_long`
--

LOCK TABLES `events_stages_history_long` WRITE;
/*!40000 ALTER TABLE `events_stages_history_long` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_history_long` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_summary_by_account_by_event_name`
--

DROP TABLE IF EXISTS `events_stages_summary_by_account_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_summary_by_account_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_summary_by_account_by_event_name`
--

LOCK TABLES `events_stages_summary_by_account_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_stages_summary_by_account_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_summary_by_account_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_summary_by_host_by_event_name`
--

DROP TABLE IF EXISTS `events_stages_summary_by_host_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_summary_by_host_by_event_name` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `HOST` (`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_summary_by_host_by_event_name`
--

LOCK TABLES `events_stages_summary_by_host_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_stages_summary_by_host_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_summary_by_host_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_summary_by_thread_by_event_name`
--

DROP TABLE IF EXISTS `events_stages_summary_by_thread_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_summary_by_thread_by_event_name` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_summary_by_thread_by_event_name`
--

LOCK TABLES `events_stages_summary_by_thread_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_stages_summary_by_thread_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_summary_by_thread_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_summary_by_user_by_event_name`
--

DROP TABLE IF EXISTS `events_stages_summary_by_user_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_summary_by_user_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `USER` (`USER`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_summary_by_user_by_event_name`
--

LOCK TABLES `events_stages_summary_by_user_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_stages_summary_by_user_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_summary_by_user_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_stages_summary_global_by_event_name`
--

DROP TABLE IF EXISTS `events_stages_summary_global_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_stages_summary_global_by_event_name` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  PRIMARY KEY (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_stages_summary_global_by_event_name`
--

LOCK TABLES `events_stages_summary_global_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_stages_summary_global_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_stages_summary_global_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_current`
--

DROP TABLE IF EXISTS `events_statements_current`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_current` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `LOCK_TIME` bigint unsigned NOT NULL,
  `SQL_TEXT` longtext,
  `DIGEST` varchar(64) DEFAULT NULL,
  `DIGEST_TEXT` longtext,
  `CURRENT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `MYSQL_ERRNO` int DEFAULT NULL,
  `RETURNED_SQLSTATE` varchar(5) DEFAULT NULL,
  `MESSAGE_TEXT` varchar(128) DEFAULT NULL,
  `ERRORS` bigint unsigned NOT NULL,
  `WARNINGS` bigint unsigned NOT NULL,
  `ROWS_AFFECTED` bigint unsigned NOT NULL,
  `ROWS_SENT` bigint unsigned NOT NULL,
  `ROWS_EXAMINED` bigint unsigned NOT NULL,
  `CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SELECT_RANGE` bigint unsigned NOT NULL,
  `SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SELECT_SCAN` bigint unsigned NOT NULL,
  `SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SORT_RANGE` bigint unsigned NOT NULL,
  `SORT_ROWS` bigint unsigned NOT NULL,
  `SORT_SCAN` bigint unsigned NOT NULL,
  `NO_INDEX_USED` bigint unsigned NOT NULL,
  `NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `NESTING_EVENT_LEVEL` int DEFAULT NULL,
  `STATEMENT_ID` bigint unsigned DEFAULT NULL,
  `CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `EXECUTION_ENGINE` enum('PRIMARY','SECONDARY') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_current`
--

LOCK TABLES `events_statements_current` WRITE;
/*!40000 ALTER TABLE `events_statements_current` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_current` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_histogram_by_digest`
--

DROP TABLE IF EXISTS `events_statements_histogram_by_digest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_histogram_by_digest` (
  `SCHEMA_NAME` varchar(64) DEFAULT NULL,
  `DIGEST` varchar(64) DEFAULT NULL,
  `BUCKET_NUMBER` int unsigned NOT NULL,
  `BUCKET_TIMER_LOW` bigint unsigned NOT NULL,
  `BUCKET_TIMER_HIGH` bigint unsigned NOT NULL,
  `COUNT_BUCKET` bigint unsigned NOT NULL,
  `COUNT_BUCKET_AND_LOWER` bigint unsigned NOT NULL,
  `BUCKET_QUANTILE` double(7,6) NOT NULL,
  UNIQUE KEY `SCHEMA_NAME` (`SCHEMA_NAME`,`DIGEST`,`BUCKET_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_histogram_by_digest`
--

LOCK TABLES `events_statements_histogram_by_digest` WRITE;
/*!40000 ALTER TABLE `events_statements_histogram_by_digest` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_histogram_by_digest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_histogram_global`
--

DROP TABLE IF EXISTS `events_statements_histogram_global`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_histogram_global` (
  `BUCKET_NUMBER` int unsigned NOT NULL,
  `BUCKET_TIMER_LOW` bigint unsigned NOT NULL,
  `BUCKET_TIMER_HIGH` bigint unsigned NOT NULL,
  `COUNT_BUCKET` bigint unsigned NOT NULL,
  `COUNT_BUCKET_AND_LOWER` bigint unsigned NOT NULL,
  `BUCKET_QUANTILE` double(7,6) NOT NULL,
  PRIMARY KEY (`BUCKET_NUMBER`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_histogram_global`
--

LOCK TABLES `events_statements_histogram_global` WRITE;
/*!40000 ALTER TABLE `events_statements_histogram_global` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_histogram_global` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_history`
--

DROP TABLE IF EXISTS `events_statements_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_history` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `LOCK_TIME` bigint unsigned NOT NULL,
  `SQL_TEXT` longtext,
  `DIGEST` varchar(64) DEFAULT NULL,
  `DIGEST_TEXT` longtext,
  `CURRENT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `MYSQL_ERRNO` int DEFAULT NULL,
  `RETURNED_SQLSTATE` varchar(5) DEFAULT NULL,
  `MESSAGE_TEXT` varchar(128) DEFAULT NULL,
  `ERRORS` bigint unsigned NOT NULL,
  `WARNINGS` bigint unsigned NOT NULL,
  `ROWS_AFFECTED` bigint unsigned NOT NULL,
  `ROWS_SENT` bigint unsigned NOT NULL,
  `ROWS_EXAMINED` bigint unsigned NOT NULL,
  `CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SELECT_RANGE` bigint unsigned NOT NULL,
  `SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SELECT_SCAN` bigint unsigned NOT NULL,
  `SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SORT_RANGE` bigint unsigned NOT NULL,
  `SORT_ROWS` bigint unsigned NOT NULL,
  `SORT_SCAN` bigint unsigned NOT NULL,
  `NO_INDEX_USED` bigint unsigned NOT NULL,
  `NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `NESTING_EVENT_LEVEL` int DEFAULT NULL,
  `STATEMENT_ID` bigint unsigned DEFAULT NULL,
  `CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `EXECUTION_ENGINE` enum('PRIMARY','SECONDARY') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_history`
--

LOCK TABLES `events_statements_history` WRITE;
/*!40000 ALTER TABLE `events_statements_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_history_long`
--

DROP TABLE IF EXISTS `events_statements_history_long`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_history_long` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `LOCK_TIME` bigint unsigned NOT NULL,
  `SQL_TEXT` longtext,
  `DIGEST` varchar(64) DEFAULT NULL,
  `DIGEST_TEXT` longtext,
  `CURRENT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `MYSQL_ERRNO` int DEFAULT NULL,
  `RETURNED_SQLSTATE` varchar(5) DEFAULT NULL,
  `MESSAGE_TEXT` varchar(128) DEFAULT NULL,
  `ERRORS` bigint unsigned NOT NULL,
  `WARNINGS` bigint unsigned NOT NULL,
  `ROWS_AFFECTED` bigint unsigned NOT NULL,
  `ROWS_SENT` bigint unsigned NOT NULL,
  `ROWS_EXAMINED` bigint unsigned NOT NULL,
  `CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SELECT_RANGE` bigint unsigned NOT NULL,
  `SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SELECT_SCAN` bigint unsigned NOT NULL,
  `SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SORT_RANGE` bigint unsigned NOT NULL,
  `SORT_ROWS` bigint unsigned NOT NULL,
  `SORT_SCAN` bigint unsigned NOT NULL,
  `NO_INDEX_USED` bigint unsigned NOT NULL,
  `NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `NESTING_EVENT_LEVEL` int DEFAULT NULL,
  `STATEMENT_ID` bigint unsigned DEFAULT NULL,
  `CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `EXECUTION_ENGINE` enum('PRIMARY','SECONDARY') DEFAULT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_history_long`
--

LOCK TABLES `events_statements_history_long` WRITE;
/*!40000 ALTER TABLE `events_statements_history_long` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_history_long` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_account_by_event_name`
--

DROP TABLE IF EXISTS `events_statements_summary_by_account_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_account_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_account_by_event_name`
--

LOCK TABLES `events_statements_summary_by_account_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_account_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_account_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_digest`
--

DROP TABLE IF EXISTS `events_statements_summary_by_digest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_digest` (
  `SCHEMA_NAME` varchar(64) DEFAULT NULL,
  `DIGEST` varchar(64) DEFAULT NULL,
  `DIGEST_TEXT` longtext,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  `FIRST_SEEN` timestamp(6) NOT NULL,
  `LAST_SEEN` timestamp(6) NOT NULL,
  `QUANTILE_95` bigint unsigned NOT NULL,
  `QUANTILE_99` bigint unsigned NOT NULL,
  `QUANTILE_999` bigint unsigned NOT NULL,
  `QUERY_SAMPLE_TEXT` longtext,
  `QUERY_SAMPLE_SEEN` timestamp(6) NOT NULL,
  `QUERY_SAMPLE_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `SCHEMA_NAME` (`SCHEMA_NAME`,`DIGEST`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_digest`
--

LOCK TABLES `events_statements_summary_by_digest` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_digest` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_digest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_host_by_event_name`
--

DROP TABLE IF EXISTS `events_statements_summary_by_host_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_host_by_event_name` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  UNIQUE KEY `HOST` (`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_host_by_event_name`
--

LOCK TABLES `events_statements_summary_by_host_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_host_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_host_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_program`
--

DROP TABLE IF EXISTS `events_statements_summary_by_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_program` (
  `OBJECT_TYPE` enum('EVENT','FUNCTION','PROCEDURE','TABLE','TRIGGER') NOT NULL,
  `OBJECT_SCHEMA` varchar(64) NOT NULL,
  `OBJECT_NAME` varchar(64) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_STATEMENTS` bigint unsigned NOT NULL,
  `SUM_STATEMENTS_WAIT` bigint unsigned NOT NULL,
  `MIN_STATEMENTS_WAIT` bigint unsigned NOT NULL,
  `AVG_STATEMENTS_WAIT` bigint unsigned NOT NULL,
  `MAX_STATEMENTS_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  PRIMARY KEY (`OBJECT_TYPE`,`OBJECT_SCHEMA`,`OBJECT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_program`
--

LOCK TABLES `events_statements_summary_by_program` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_program` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_thread_by_event_name`
--

DROP TABLE IF EXISTS `events_statements_summary_by_thread_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_thread_by_event_name` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_thread_by_event_name`
--

LOCK TABLES `events_statements_summary_by_thread_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_thread_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_thread_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_by_user_by_event_name`
--

DROP TABLE IF EXISTS `events_statements_summary_by_user_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_by_user_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  UNIQUE KEY `USER` (`USER`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_by_user_by_event_name`
--

LOCK TABLES `events_statements_summary_by_user_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_by_user_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_by_user_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_statements_summary_global_by_event_name`
--

DROP TABLE IF EXISTS `events_statements_summary_global_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_statements_summary_global_by_event_name` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `SUM_LOCK_TIME` bigint unsigned NOT NULL,
  `SUM_ERRORS` bigint unsigned NOT NULL,
  `SUM_WARNINGS` bigint unsigned NOT NULL,
  `SUM_ROWS_AFFECTED` bigint unsigned NOT NULL,
  `SUM_ROWS_SENT` bigint unsigned NOT NULL,
  `SUM_ROWS_EXAMINED` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_DISK_TABLES` bigint unsigned NOT NULL,
  `SUM_CREATED_TMP_TABLES` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_FULL_RANGE_JOIN` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE` bigint unsigned NOT NULL,
  `SUM_SELECT_RANGE_CHECK` bigint unsigned NOT NULL,
  `SUM_SELECT_SCAN` bigint unsigned NOT NULL,
  `SUM_SORT_MERGE_PASSES` bigint unsigned NOT NULL,
  `SUM_SORT_RANGE` bigint unsigned NOT NULL,
  `SUM_SORT_ROWS` bigint unsigned NOT NULL,
  `SUM_SORT_SCAN` bigint unsigned NOT NULL,
  `SUM_NO_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_NO_GOOD_INDEX_USED` bigint unsigned NOT NULL,
  `SUM_CPU_TIME` bigint unsigned NOT NULL,
  `MAX_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_TOTAL_MEMORY` bigint unsigned NOT NULL,
  `COUNT_SECONDARY` bigint unsigned NOT NULL,
  PRIMARY KEY (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_statements_summary_global_by_event_name`
--

LOCK TABLES `events_statements_summary_global_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_statements_summary_global_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_statements_summary_global_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_current`
--

DROP TABLE IF EXISTS `events_transactions_current`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_current` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `STATE` enum('ACTIVE','COMMITTED','ROLLED BACK') DEFAULT NULL,
  `TRX_ID` bigint unsigned DEFAULT NULL,
  `GTID` varchar(64) DEFAULT NULL,
  `XID_FORMAT_ID` int DEFAULT NULL,
  `XID_GTRID` varchar(130) DEFAULT NULL,
  `XID_BQUAL` varchar(130) DEFAULT NULL,
  `XA_STATE` varchar(64) DEFAULT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `ACCESS_MODE` enum('READ ONLY','READ WRITE') DEFAULT NULL,
  `ISOLATION_LEVEL` varchar(64) DEFAULT NULL,
  `AUTOCOMMIT` enum('YES','NO') NOT NULL,
  `NUMBER_OF_SAVEPOINTS` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_ROLLBACK_TO_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_RELEASE_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_current`
--

LOCK TABLES `events_transactions_current` WRITE;
/*!40000 ALTER TABLE `events_transactions_current` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_current` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_history`
--

DROP TABLE IF EXISTS `events_transactions_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_history` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `STATE` enum('ACTIVE','COMMITTED','ROLLED BACK') DEFAULT NULL,
  `TRX_ID` bigint unsigned DEFAULT NULL,
  `GTID` varchar(64) DEFAULT NULL,
  `XID_FORMAT_ID` int DEFAULT NULL,
  `XID_GTRID` varchar(130) DEFAULT NULL,
  `XID_BQUAL` varchar(130) DEFAULT NULL,
  `XA_STATE` varchar(64) DEFAULT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `ACCESS_MODE` enum('READ ONLY','READ WRITE') DEFAULT NULL,
  `ISOLATION_LEVEL` varchar(64) DEFAULT NULL,
  `AUTOCOMMIT` enum('YES','NO') NOT NULL,
  `NUMBER_OF_SAVEPOINTS` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_ROLLBACK_TO_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_RELEASE_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_history`
--

LOCK TABLES `events_transactions_history` WRITE;
/*!40000 ALTER TABLE `events_transactions_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_history_long`
--

DROP TABLE IF EXISTS `events_transactions_history_long`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_history_long` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `STATE` enum('ACTIVE','COMMITTED','ROLLED BACK') DEFAULT NULL,
  `TRX_ID` bigint unsigned DEFAULT NULL,
  `GTID` varchar(64) DEFAULT NULL,
  `XID_FORMAT_ID` int DEFAULT NULL,
  `XID_GTRID` varchar(130) DEFAULT NULL,
  `XID_BQUAL` varchar(130) DEFAULT NULL,
  `XA_STATE` varchar(64) DEFAULT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `ACCESS_MODE` enum('READ ONLY','READ WRITE') DEFAULT NULL,
  `ISOLATION_LEVEL` varchar(64) DEFAULT NULL,
  `AUTOCOMMIT` enum('YES','NO') NOT NULL,
  `NUMBER_OF_SAVEPOINTS` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_ROLLBACK_TO_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `NUMBER_OF_RELEASE_SAVEPOINT` bigint unsigned DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_history_long`
--

LOCK TABLES `events_transactions_history_long` WRITE;
/*!40000 ALTER TABLE `events_transactions_history_long` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_history_long` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_summary_by_account_by_event_name`
--

DROP TABLE IF EXISTS `events_transactions_summary_by_account_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_summary_by_account_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `COUNT_READ_ONLY` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_summary_by_account_by_event_name`
--

LOCK TABLES `events_transactions_summary_by_account_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_transactions_summary_by_account_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_summary_by_account_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_summary_by_host_by_event_name`
--

DROP TABLE IF EXISTS `events_transactions_summary_by_host_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_summary_by_host_by_event_name` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `COUNT_READ_ONLY` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  UNIQUE KEY `HOST` (`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_summary_by_host_by_event_name`
--

LOCK TABLES `events_transactions_summary_by_host_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_transactions_summary_by_host_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_summary_by_host_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_summary_by_thread_by_event_name`
--

DROP TABLE IF EXISTS `events_transactions_summary_by_thread_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_summary_by_thread_by_event_name` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `COUNT_READ_ONLY` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_summary_by_thread_by_event_name`
--

LOCK TABLES `events_transactions_summary_by_thread_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_transactions_summary_by_thread_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_summary_by_thread_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_summary_by_user_by_event_name`
--

DROP TABLE IF EXISTS `events_transactions_summary_by_user_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_summary_by_user_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `COUNT_READ_ONLY` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  UNIQUE KEY `USER` (`USER`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_summary_by_user_by_event_name`
--

LOCK TABLES `events_transactions_summary_by_user_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_transactions_summary_by_user_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_summary_by_user_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_transactions_summary_global_by_event_name`
--

DROP TABLE IF EXISTS `events_transactions_summary_global_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_transactions_summary_global_by_event_name` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_WRITE` bigint unsigned NOT NULL,
  `COUNT_READ_ONLY` bigint unsigned NOT NULL,
  `SUM_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MIN_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `AVG_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  `MAX_TIMER_READ_ONLY` bigint unsigned NOT NULL,
  PRIMARY KEY (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_transactions_summary_global_by_event_name`
--

LOCK TABLES `events_transactions_summary_global_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_transactions_summary_global_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_transactions_summary_global_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_current`
--

DROP TABLE IF EXISTS `events_waits_current`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_current` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `SPINS` int unsigned DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(512) DEFAULT NULL,
  `INDEX_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `OPERATION` varchar(32) NOT NULL,
  `NUMBER_OF_BYTES` bigint DEFAULT NULL,
  `FLAGS` int unsigned DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_current`
--

LOCK TABLES `events_waits_current` WRITE;
/*!40000 ALTER TABLE `events_waits_current` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_current` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_history`
--

DROP TABLE IF EXISTS `events_waits_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_history` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `SPINS` int unsigned DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(512) DEFAULT NULL,
  `INDEX_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `OPERATION` varchar(32) NOT NULL,
  `NUMBER_OF_BYTES` bigint DEFAULT NULL,
  `FLAGS` int unsigned DEFAULT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_ID`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_history`
--

LOCK TABLES `events_waits_history` WRITE;
/*!40000 ALTER TABLE `events_waits_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_history_long`
--

DROP TABLE IF EXISTS `events_waits_history_long`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_history_long` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_ID` bigint unsigned NOT NULL,
  `END_EVENT_ID` bigint unsigned DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TIMER_START` bigint unsigned DEFAULT NULL,
  `TIMER_END` bigint unsigned DEFAULT NULL,
  `TIMER_WAIT` bigint unsigned DEFAULT NULL,
  `SPINS` int unsigned DEFAULT NULL,
  `OBJECT_SCHEMA` varchar(64) DEFAULT NULL,
  `OBJECT_NAME` varchar(512) DEFAULT NULL,
  `INDEX_NAME` varchar(64) DEFAULT NULL,
  `OBJECT_TYPE` varchar(64) DEFAULT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `NESTING_EVENT_ID` bigint unsigned DEFAULT NULL,
  `NESTING_EVENT_TYPE` enum('TRANSACTION','STATEMENT','STAGE','WAIT') DEFAULT NULL,
  `OPERATION` varchar(32) NOT NULL,
  `NUMBER_OF_BYTES` bigint DEFAULT NULL,
  `FLAGS` int unsigned DEFAULT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_history_long`
--

LOCK TABLES `events_waits_history_long` WRITE;
/*!40000 ALTER TABLE `events_waits_history_long` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_history_long` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_by_account_by_event_name`
--

DROP TABLE IF EXISTS `events_waits_summary_by_account_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_by_account_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `ACCOUNT` (`USER`,`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_by_account_by_event_name`
--

LOCK TABLES `events_waits_summary_by_account_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_by_account_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_by_account_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_by_host_by_event_name`
--

DROP TABLE IF EXISTS `events_waits_summary_by_host_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_by_host_by_event_name` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `HOST` (`HOST`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_by_host_by_event_name`
--

LOCK TABLES `events_waits_summary_by_host_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_by_host_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_by_host_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_by_instance`
--

DROP TABLE IF EXISTS `events_waits_summary_by_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_by_instance` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  PRIMARY KEY (`OBJECT_INSTANCE_BEGIN`),
  KEY `EVENT_NAME` (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_by_instance`
--

LOCK TABLES `events_waits_summary_by_instance` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_by_instance` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_by_instance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_by_thread_by_event_name`
--

DROP TABLE IF EXISTS `events_waits_summary_by_thread_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_by_thread_by_event_name` (
  `THREAD_ID` bigint unsigned NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  PRIMARY KEY (`THREAD_ID`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_by_thread_by_event_name`
--

LOCK TABLES `events_waits_summary_by_thread_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_by_thread_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_by_thread_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_by_user_by_event_name`
--

DROP TABLE IF EXISTS `events_waits_summary_by_user_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_by_user_by_event_name` (
  `USER` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  UNIQUE KEY `USER` (`USER`,`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_by_user_by_event_name`
--

LOCK TABLES `events_waits_summary_by_user_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_by_user_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_by_user_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_waits_summary_global_by_event_name`
--

DROP TABLE IF EXISTS `events_waits_summary_global_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_waits_summary_global_by_event_name` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  PRIMARY KEY (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_waits_summary_global_by_event_name`
--

LOCK TABLES `events_waits_summary_global_by_event_name` WRITE;
/*!40000 ALTER TABLE `events_waits_summary_global_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_waits_summary_global_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_instances`
--

DROP TABLE IF EXISTS `file_instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_instances` (
  `FILE_NAME` varchar(512) NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `OPEN_COUNT` int unsigned NOT NULL,
  PRIMARY KEY (`FILE_NAME`),
  KEY `EVENT_NAME` (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_instances`
--

LOCK TABLES `file_instances` WRITE;
/*!40000 ALTER TABLE `file_instances` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_instances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_summary_by_event_name`
--

DROP TABLE IF EXISTS `file_summary_by_event_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_summary_by_event_name` (
  `EVENT_NAME` varchar(128) NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ` bigint unsigned NOT NULL,
  `SUM_TIMER_READ` bigint unsigned NOT NULL,
  `MIN_TIMER_READ` bigint unsigned NOT NULL,
  `AVG_TIMER_READ` bigint unsigned NOT NULL,
  `MAX_TIMER_READ` bigint unsigned NOT NULL,
  `SUM_NUMBER_OF_BYTES_READ` bigint NOT NULL,
  `COUNT_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_WRITE` bigint unsigned NOT NULL,
  `SUM_NUMBER_OF_BYTES_WRITE` bigint NOT NULL,
  `COUNT_MISC` bigint unsigned NOT NULL,
  `SUM_TIMER_MISC` bigint unsigned NOT NULL,
  `MIN_TIMER_MISC` bigint unsigned NOT NULL,
  `AVG_TIMER_MISC` bigint unsigned NOT NULL,
  `MAX_TIMER_MISC` bigint unsigned NOT NULL,
  PRIMARY KEY (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_summary_by_event_name`
--

LOCK TABLES `file_summary_by_event_name` WRITE;
/*!40000 ALTER TABLE `file_summary_by_event_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_summary_by_event_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_summary_by_instance`
--

DROP TABLE IF EXISTS `file_summary_by_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_summary_by_instance` (
  `FILE_NAME` varchar(512) NOT NULL,
  `EVENT_NAME` varchar(128) NOT NULL,
  `OBJECT_INSTANCE_BEGIN` bigint unsigned NOT NULL,
  `COUNT_STAR` bigint unsigned NOT NULL,
  `SUM_TIMER_WAIT` bigint unsigned NOT NULL,
  `MIN_TIMER_WAIT` bigint unsigned NOT NULL,
  `AVG_TIMER_WAIT` bigint unsigned NOT NULL,
  `MAX_TIMER_WAIT` bigint unsigned NOT NULL,
  `COUNT_READ` bigint unsigned NOT NULL,
  `SUM_TIMER_READ` bigint unsigned NOT NULL,
  `MIN_TIMER_READ` bigint unsigned NOT NULL,
  `AVG_TIMER_READ` bigint unsigned NOT NULL,
  `MAX_TIMER_READ` bigint unsigned NOT NULL,
  `SUM_NUMBER_OF_BYTES_READ` bigint NOT NULL,
  `COUNT_WRITE` bigint unsigned NOT NULL,
  `SUM_TIMER_WRITE` bigint unsigned NOT NULL,
  `MIN_TIMER_WRITE` bigint unsigned NOT NULL,
  `AVG_TIMER_WRITE` bigint unsigned NOT NULL,
  `MAX_TIMER_WRITE` bigint unsigned NOT NULL,
  `SUM_NUMBER_OF_BYTES_WRITE` bigint NOT NULL,
  `COUNT_MISC` bigint unsigned NOT NULL,
  `SUM_TIMER_MISC` bigint unsigned NOT NULL,
  `MIN_TIMER_MISC` bigint unsigned NOT NULL,
  `AVG_TIMER_MISC` bigint unsigned NOT NULL,
  `MAX_TIMER_MISC` bigint unsigned NOT NULL,
  PRIMARY KEY (`OBJECT_INSTANCE_BEGIN`),
  KEY `FILE_NAME` (`FILE_NAME`),
  KEY `EVENT_NAME` (`EVENT_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_summary_by_instance`
--

LOCK TABLES `file_summary_by_instance` WRITE;
/*!40000 ALTER TABLE `file_summary_by_instance` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_summary_by_instance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `global_status`
--

DROP TABLE IF EXISTS `global_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `global_status` (
  `VARIABLE_NAME` varchar(64) NOT NULL,
  `VARIABLE_VALUE` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`VARIABLE_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `global_status`
--

LOCK TABLES `global_status` WRITE;
/*!40000 ALTER TABLE `global_status` DISABLE KEYS */;
INSERT INTO `global_status` VALUES
('Aborted_clients','31'),
('Aborted_connects','3334'),
('Acl_cache_items_count','1'),
('Binlog_cache_disk_use','0'),
('Binlog_cache_use','0'),
('Binlog_stmt_cache_disk_use','0'),
('Binlog_stmt_cache_use','0'),
('Bytes_received','97932166'),
('Bytes_sent','155147815'),
('Caching_sha2_password_rsa_public_key','-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAptqydIS5Cv8cPckLQf0f\nPbqT+IBfP9ldUjB8pcGTRZg3tZtbwr9qhalFOjgPFZY6KwHU+pVjMr45f6S+3giH\n1wpwt4ZOignnnSIB3UVvcCLTA1ewHg8NHBWAl1ryiwDh1ZbmAewYxvxmdjlG9N5f\nF7a8HBClhybYg//IEW7CskW/VTIFZOfP7EvJ/yMGhzhBEodgDjMd2lVOEPUM0mlk\nl+SXWewl827m+dglIpc7ruHXI275vZHO9fQf8bOD7RJpQ4ItUy4orUwRqOL+WAi3\nUq2gfCNSYR/8N+C2xvWuHPKNpp1A4+5NG8ZGVU6rVpSjG3FzQRY5XQpgY325uilp\ntwIDAQAB\n-----END PUBLIC KEY-----\n'),
('Com_stmt_reprepare','0'),
('Connection_errors_accept','0'),
('Connection_errors_internal','0'),
('Connection_errors_max_connections','0'),
('Connection_errors_peer_address','0'),
('Connection_errors_select','0'),
('Connection_errors_tcpwrap','0'),
('Connections','13489'),
('Created_tmp_disk_tables','8512'),
('Created_tmp_files','5'),
('Created_tmp_tables','53789'),
('Current_tls_ca','/rdsdbdata/rds-metadata/ca-cert.pem'),
('Current_tls_capath',''),
('Current_tls_cert','/rdsdbdata/rds-metadata/server-cert.pem'),
('Current_tls_cipher',''),
('Current_tls_ciphersuites',''),
('Current_tls_crl',''),
('Current_tls_crlpath',''),
('Current_tls_key','/rdsdbdata/rds-metadata/server-key.pem'),
('Current_tls_version','TLSv1.2,TLSv1.3'),
('Delayed_errors','0'),
('Delayed_insert_threads','0'),
('Delayed_writes','0'),
('Deprecated_use_i_s_processlist_count','4240'),
('Deprecated_use_i_s_processlist_last_timestamp','1749887686628639'),
('Error_log_buffered_bytes','117000'),
('Error_log_buffered_events','634'),
('Error_log_expired_events','0'),
('Error_log_latest_write','1749887469752790'),
('Flush_commands','3'),
('Global_connection_memory','0'),
('Handler_commit','318597'),
('Handler_delete','4286'),
('Handler_discover','0'),
('Handler_external_lock','1897983'),
('Handler_mrr_init','0'),
('Handler_prepare','0'),
('Handler_read_first','270209'),
('Handler_read_key','985790'),
('Handler_read_last','0'),
('Handler_read_next','550194'),
('Handler_read_prev','404'),
('Handler_read_rnd','12435'),
('Handler_read_rnd_next','1770069'),
('Handler_rollback','60'),
('Handler_savepoint','2'),
('Handler_savepoint_rollback','146'),
('Handler_update','25021'),
('Handler_write','406897'),
('Innodb_buffer_pool_dump_status','Dumping of buffer pool not started'),
('Innodb_buffer_pool_load_status','Buffer pool(s) load completed at 250530 14:45:01'),
('Innodb_buffer_pool_resize_status',''),
('Innodb_buffer_pool_resize_status_code','0'),
('Innodb_buffer_pool_resize_status_progress','0'),
('Innodb_buffer_pool_pages_data','2939'),
('Innodb_buffer_pool_bytes_data','48152576'),
('Innodb_buffer_pool_pages_dirty','0'),
('Innodb_buffer_pool_bytes_dirty','0'),
('Innodb_buffer_pool_pages_flushed','87739'),
('Innodb_buffer_pool_pages_free','13414'),
('Innodb_buffer_pool_pages_misc','31'),
('Innodb_buffer_pool_pages_total','16384'),
('Innodb_buffer_pool_read_ahead_rnd','0'),
('Innodb_buffer_pool_read_ahead','0'),
('Innodb_buffer_pool_read_ahead_evicted','0'),
('Innodb_buffer_pool_read_requests','6254639'),
('Innodb_buffer_pool_reads','1129'),
('Innodb_buffer_pool_wait_free','0'),
('Innodb_buffer_pool_write_requests','998875'),
('Innodb_data_fsyncs','120216'),
('Innodb_data_pending_fsyncs','0'),
('Innodb_data_pending_reads','0'),
('Innodb_data_pending_writes','0'),
('Innodb_data_read','18565632'),
('Innodb_data_reads','1149'),
('Innodb_data_writes','193125'),
('Innodb_data_written','1523725824'),
('Innodb_dblwr_pages_written','78796'),
('Innodb_dblwr_writes','19054'),
('Innodb_redo_log_read_only','OFF'),
('Innodb_redo_log_uuid','1236400582'),
('Innodb_redo_log_checkpoint_lsn','62911242'),
('Innodb_redo_log_current_lsn','62911242'),
('Innodb_redo_log_flushed_to_disk_lsn','62911242'),
('Innodb_redo_log_logical_size','512'),
('Innodb_redo_log_physical_size','67108864'),
('Innodb_redo_log_capacity_resized','2147483648'),
('Innodb_redo_log_resize_status','OK'),
('Innodb_log_waits','0'),
('Innodb_log_write_requests','548500'),
('Innodb_log_writes','67347'),
('Innodb_os_log_fsyncs','78951'),
('Innodb_os_log_pending_fsyncs','0'),
('Innodb_os_log_pending_writes','0'),
('Innodb_os_log_written','58315264'),
('Innodb_page_size','16384'),
('Innodb_pages_created','8746'),
('Innodb_pages_read','1128'),
('Innodb_pages_written','87740'),
('Innodb_redo_log_enabled','ON'),
('Innodb_row_lock_current_waits','0'),
('Innodb_row_lock_time','0'),
('Innodb_row_lock_time_avg','0'),
('Innodb_row_lock_time_max','0'),
('Innodb_row_lock_waits','0'),
('Innodb_rows_deleted','391'),
('Innodb_rows_inserted','218883'),
('Innodb_rows_read','1078541'),
('Innodb_rows_updated','4040'),
('Innodb_system_rows_deleted','3917'),
('Innodb_system_rows_inserted','144129'),
('Innodb_system_rows_read','1457152'),
('Innodb_system_rows_updated','21517'),
('Innodb_sampled_pages_read','0'),
('Innodb_sampled_pages_skipped','0'),
('Innodb_num_open_files','95'),
('Innodb_truncated_status_writes','0'),
('Innodb_undo_tablespaces_total','2'),
('Innodb_undo_tablespaces_implicit','2'),
('Innodb_undo_tablespaces_explicit','0'),
('Innodb_undo_tablespaces_active','2'),
('Key_blocks_not_flushed','0'),
('Key_blocks_unused','13396'),
('Key_blocks_used','0'),
('Key_read_requests','0'),
('Key_reads','0'),
('Key_write_requests','0'),
('Key_writes','0'),
('Locked_connects','0'),
('Max_execution_time_exceeded','0'),
('Max_execution_time_set','0'),
('Max_execution_time_set_failed','0'),
('Max_used_connections','21'),
('Max_used_connections_time','2025-06-03 05:57:13'),
('Not_flushed_delayed_rows','0'),
('Ongoing_anonymous_transaction_count','0'),
('Open_files','8'),
('Open_streams','0'),
('Open_table_definitions','226'),
('Open_tables','1810'),
('Opened_files','8'),
('Opened_table_definitions','961'),
('Opened_tables','2361'),
('Performance_schema_accounts_lost','0'),
('Performance_schema_cond_classes_lost','0'),
('Performance_schema_cond_instances_lost','0'),
('Performance_schema_digest_lost','0'),
('Performance_schema_file_classes_lost','0'),
('Performance_schema_file_handles_lost','0'),
('Performance_schema_file_instances_lost','0'),
('Performance_schema_hosts_lost','0'),
('Performance_schema_index_stat_lost','0'),
('Performance_schema_locker_lost','0'),
('Performance_schema_memory_classes_lost','0'),
('Performance_schema_metadata_lock_lost','0'),
('Performance_schema_mutex_classes_lost','0'),
('Performance_schema_mutex_instances_lost','0'),
('Performance_schema_nested_statement_lost','0'),
('Performance_schema_prepared_statements_lost','0'),
('Performance_schema_program_lost','0'),
('Performance_schema_rwlock_classes_lost','0'),
('Performance_schema_rwlock_instances_lost','0'),
('Performance_schema_session_connect_attrs_longest_seen','0'),
('Performance_schema_session_connect_attrs_lost','0'),
('Performance_schema_socket_classes_lost','0'),
('Performance_schema_socket_instances_lost','0'),
('Performance_schema_stage_classes_lost','0'),
('Performance_schema_statement_classes_lost','0'),
('Performance_schema_table_handles_lost','0'),
('Performance_schema_table_instances_lost','0'),
('Performance_schema_table_lock_stat_lost','0'),
('Performance_schema_thread_classes_lost','0'),
('Performance_schema_thread_instances_lost','0'),
('Performance_schema_users_lost','0'),
('Prepared_stmt_count','0'),
('Queries','1593693'),
('Questions','1588047'),
('Replica_open_temp_tables','0'),
('Resource_group_supported','ON'),
('Rsa_public_key','-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAptqydIS5Cv8cPckLQf0f\nPbqT+IBfP9ldUjB8pcGTRZg3tZtbwr9qhalFOjgPFZY6KwHU+pVjMr45f6S+3giH\n1wpwt4ZOignnnSIB3UVvcCLTA1ewHg8NHBWAl1ryiwDh1ZbmAewYxvxmdjlG9N5f\nF7a8HBClhybYg//IEW7CskW/VTIFZOfP7EvJ/yMGhzhBEodgDjMd2lVOEPUM0mlk\nl+SXWewl827m+dglIpc7ruHXI275vZHO9fQf8bOD7RJpQ4ItUy4orUwRqOL+WAi3\nUq2gfCNSYR/8N+C2xvWuHPKNpp1A4+5NG8ZGVU6rVpSjG3FzQRY5XQpgY325uilp\ntwIDAQAB\n-----END PUBLIC KEY-----\n'),
('Secondary_engine_execution_count','0'),
('Select_full_join','3082'),
('Select_full_range_join','0'),
('Select_range','2261'),
('Select_range_check','0'),
('Select_scan','265304'),
('Slave_open_temp_tables','0'),
('Slow_launch_threads','0'),
('Slow_queries','2'),
('Sort_merge_passes','0'),
('Sort_range','0'),
('Sort_rows','31995'),
('Sort_scan','45309'),
('Ssl_accept_renegotiates','0'),
('Ssl_accepts','597'),
('Ssl_callback_cache_hits','0'),
('Ssl_cipher','ECDHE-RSA-AES256-GCM-SHA384'),
('Ssl_cipher_list','TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:DHE-RSA-AES128-SHA256:DHE-DSS-AES128-SHA256:DHE-DSS-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-DSS-AES128-SHA:DHE-RSA-AES128-SHA:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES256-SHA:CAMELLIA256-SHA:CAMELLIA128-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA'),
('Ssl_client_connects','0'),
('Ssl_connect_renegotiates','0'),
('Ssl_ctx_verify_depth','18446744073709551615'),
('Ssl_ctx_verify_mode','5'),
('Ssl_default_timeout','7200'),
('Ssl_finished_accepts','554'),
('Ssl_finished_connects','0'),
('Ssl_server_not_after','May 30 14:44:27 2026 GMT'),
('Ssl_server_not_before','May 30 14:44:27 2025 GMT'),
('Ssl_session_cache_hits','0'),
('Ssl_session_cache_misses','0'),
('Ssl_session_cache_mode','SERVER'),
('Ssl_session_cache_overflows','0'),
('Ssl_session_cache_size','128'),
('Ssl_session_cache_timeout','300'),
('Ssl_session_cache_timeouts','0'),
('Ssl_sessions_reused','0'),
('Ssl_used_session_cache_entries','0'),
('Ssl_verify_depth','18446744073709551615'),
('Ssl_verify_mode','5'),
('Ssl_version','TLSv1.2'),
('Table_locks_immediate','51121'),
('Table_locks_waited','0'),
('Table_open_cache_hits','947770'),
('Table_open_cache_misses','2264'),
('Table_open_cache_overflows','0'),
('Tc_log_max_pages_used','0'),
('Tc_log_page_size','0'),
('Tc_log_page_waits','0'),
('Telemetry_traces_supported','ON'),
('Threads_cached','2'),
('Threads_connected','7'),
('Threads_created','699'),
('Threads_running','2'),
('Tls_library_version','OpenSSL 1.1.1za  3 Sep 2024'),
('Uptime','1271594'),
('Uptime_since_flush_status','1271594');
/*!40000 ALTER TABLE `global_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `global_variables`
--

DROP TABLE IF EXISTS `global_variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `global_variables` (
  `VARIABLE_NAME` varchar(64) NOT NULL,
  `VARIABLE_VALUE` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`VARIABLE_NAME`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `global_variables`
--

LOCK TABLES `global_variables` WRITE;
/*!40000 ALTER TABLE `global_variables` DISABLE KEYS */;
INSERT INTO `global_variables` VALUES
('activate_all_roles_on_login','OFF'),
('admin_address',''),
('admin_port','33062'),
('admin_ssl_ca',''),
('admin_ssl_capath',''),
('admin_ssl_cert',''),
('admin_ssl_cipher',''),
('admin_ssl_crl',''),
('admin_ssl_crlpath',''),
('admin_ssl_key',''),
('admin_tls_ciphersuites',''),
('admin_tls_version','TLSv1.2,TLSv1.3'),
('authentication_policy','*'),
('auto_generate_certs','ON'),
('auto_increment_increment','1'),
('auto_increment_offset','1'),
('autocommit','ON'),
('automatic_sp_privileges','ON'),
('avoid_temporal_upgrade','OFF'),
('back_log','60'),
('basedir','/rdsdbbin/mysql-8.0.41.R2/'),
('big_tables','OFF'),
('bind_address','*'),
('binlog_cache_size','32768'),
('binlog_checksum','CRC32'),
('binlog_direct_non_transactional_updates','OFF'),
('binlog_encryption','OFF'),
('binlog_error_action','ABORT_SERVER'),
('binlog_expire_logs_auto_purge','ON'),
('binlog_expire_logs_seconds','2592000'),
('binlog_format','ROW'),
('binlog_group_commit_sync_delay','0'),
('binlog_group_commit_sync_no_delay_count','0'),
('binlog_gtid_simple_recovery','ON'),
('binlog_max_flush_queue_time','0'),
('binlog_order_commits','ON'),
('binlog_rotate_encryption_master_key_at_startup','OFF'),
('binlog_row_event_max_size','8192'),
('binlog_row_image','FULL'),
('binlog_row_metadata','MINIMAL'),
('binlog_row_value_options',''),
('binlog_rows_query_log_events','OFF'),
('binlog_stmt_cache_size','32768'),
('binlog_transaction_compression','OFF'),
('binlog_transaction_compression_level_zstd','3'),
('binlog_transaction_dependency_history_size','25000'),
('binlog_transaction_dependency_tracking','COMMIT_ORDER'),
('block_encryption_mode','aes-128-ecb'),
('bulk_insert_buffer_size','8388608'),
('caching_sha2_password_auto_generate_rsa_keys','ON'),
('caching_sha2_password_digest_rounds','5000'),
('caching_sha2_password_private_key_path','private_key.pem'),
('caching_sha2_password_public_key_path','public_key.pem'),
('character_set_client','utf8mb4'),
('character_set_connection','utf8mb4'),
('character_set_database','utf8mb4'),
('character_set_filesystem','binary'),
('character_set_results','utf8mb4'),
('character_set_server','utf8mb4'),
('character_set_system','utf8mb3'),
('character_sets_dir','/rdsdbbin/mysql-8.0.41.R2/share/charsets/'),
('check_proxy_users','OFF'),
('collation_connection','utf8mb4_0900_ai_ci'),
('collation_database','utf8mb4_0900_ai_ci'),
('collation_server','utf8mb4_0900_ai_ci'),
('completion_type','NO_CHAIN'),
('concurrent_insert','AUTO'),
('connect_timeout','10'),
('connection_memory_chunk_size','8192'),
('connection_memory_limit','18446744073709551615'),
('core_file','OFF'),
('create_admin_listener_thread','OFF'),
('cte_max_recursion_depth','1000'),
('datadir','/rdsdbdata/db/'),
('default_authentication_plugin','mysql_native_password'),
('default_collation_for_utf8mb4','utf8mb4_0900_ai_ci'),
('default_password_lifetime','0'),
('default_storage_engine','InnoDB'),
('default_table_encryption','OFF'),
('default_tmp_storage_engine','InnoDB'),
('default_week_format','0'),
('delay_key_write','ON'),
('delayed_insert_limit','100'),
('delayed_insert_timeout','300'),
('delayed_queue_size','1000'),
('disabled_storage_engines',''),
('disconnect_on_expired_password','ON'),
('div_precision_increment','4'),
('end_markers_in_json','OFF'),
('enforce_gtid_consistency','OFF'),
('eq_range_index_dive_limit','200'),
('event_scheduler','ON'),
('expire_logs_days','0'),
('explain_format','TRADITIONAL'),
('explicit_defaults_for_timestamp','ON'),
('flush','OFF'),
('flush_time','0'),
('foreign_key_checks','ON'),
('ft_boolean_syntax','+ -><()~*:\"\"&|'),
('ft_max_word_len','84'),
('ft_min_word_len','4'),
('ft_query_expansion_limit','20'),
('ft_stopword_file','(built-in)'),
('general_log','OFF'),
('general_log_file','/rdsdbdata/log/general/mysql-general.log'),
('generated_random_password_length','20'),
('global_connection_memory_limit','18446744073709551615'),
('global_connection_memory_tracking','OFF'),
('group_concat_max_len','1024'),
('group_replication_consistency','EVENTUAL'),
('gtid_executed',''),
('gtid_executed_compression_period','0'),
('gtid_mode','OFF_PERMISSIVE'),
('gtid_owned',''),
('gtid_purged',''),
('have_compress','YES'),
('have_dynamic_loading','YES'),
('have_geometry','YES'),
('have_openssl','YES'),
('have_profiling','YES'),
('have_query_cache','NO'),
('have_rtree_keys','YES'),
('have_ssl','YES'),
('have_statement_timeout','YES'),
('have_symlink','DISABLED'),
('histogram_generation_max_mem_size','20000000'),
('host_cache_size','188'),
('hostname','ip-10-1-0-99'),
('information_schema_stats_expiry','86400'),
('init_connect',''),
('init_file',''),
('init_replica',''),
('init_slave',''),
('innodb_adaptive_flushing','ON'),
('innodb_adaptive_flushing_lwm','10'),
('innodb_adaptive_hash_index','ON'),
('innodb_adaptive_hash_index_parts','8'),
('innodb_adaptive_max_sleep_delay','150000'),
('innodb_api_bk_commit_interval','5'),
('innodb_api_disable_rowlock','OFF'),
('innodb_api_enable_binlog','OFF'),
('innodb_api_enable_mdl','OFF'),
('innodb_api_trx_level','0'),
('innodb_autoextend_increment','64'),
('innodb_autoinc_lock_mode','2'),
('innodb_buffer_pool_chunk_size','134217728'),
('innodb_buffer_pool_dump_at_shutdown','ON'),
('innodb_buffer_pool_dump_now','OFF'),
('innodb_buffer_pool_dump_pct','25'),
('innodb_buffer_pool_filename','ib_buffer_pool'),
('innodb_buffer_pool_in_core_file','ON'),
('innodb_buffer_pool_instances','1'),
('innodb_buffer_pool_load_abort','OFF'),
('innodb_buffer_pool_load_at_startup','ON'),
('innodb_buffer_pool_load_now','OFF'),
('innodb_buffer_pool_size','268435456'),
('innodb_change_buffer_max_size','25'),
('innodb_change_buffering','all'),
('innodb_checksum_algorithm','crc32'),
('innodb_cmp_per_index_enabled','OFF'),
('innodb_commit_concurrency','0'),
('innodb_compression_failure_threshold_pct','5'),
('innodb_compression_level','6'),
('innodb_compression_pad_pct_max','50'),
('innodb_concurrency_tickets','5000'),
('innodb_data_file_path','ibdata1:12M:autoextend'),
('innodb_data_home_dir','/rdsdbdata/db/innodb'),
('innodb_ddl_buffer_size','1048576'),
('innodb_ddl_threads','4'),
('innodb_deadlock_detect','ON'),
('innodb_dedicated_server','OFF'),
('innodb_default_row_format','dynamic'),
('innodb_directories',''),
('innodb_disable_sort_file_cache','OFF'),
('innodb_doublewrite','ON'),
('innodb_doublewrite_batch_size','16'),
('innodb_doublewrite_dir',''),
('innodb_doublewrite_files','2'),
('innodb_doublewrite_pages','32'),
('innodb_extend_and_initialize','ON'),
('innodb_fast_shutdown','1'),
('innodb_file_per_table','ON'),
('innodb_fill_factor','100'),
('innodb_flush_log_at_timeout','1'),
('innodb_flush_log_at_trx_commit','1'),
('innodb_flush_method','O_DIRECT'),
('innodb_flush_neighbors','0'),
('innodb_flush_sync','ON'),
('innodb_flushing_avg_loops','30'),
('innodb_force_load_corrupted','OFF'),
('innodb_force_recovery','0'),
('innodb_fsync_threshold','0'),
('innodb_ft_aux_table',''),
('innodb_ft_cache_size','8000000'),
('innodb_ft_enable_diag_print','OFF'),
('innodb_ft_enable_stopword','ON'),
('innodb_ft_max_token_size','84'),
('innodb_ft_min_token_size','3'),
('innodb_ft_num_word_optimize','2000'),
('innodb_ft_result_cache_limit','2000000000'),
('innodb_ft_server_stopword_table',''),
('innodb_ft_sort_pll_degree','2'),
('innodb_ft_total_cache_size','640000000'),
('innodb_ft_user_stopword_table',''),
('innodb_idle_flush_pct','100'),
('innodb_io_capacity','200'),
('innodb_io_capacity_max','2000'),
('innodb_lock_wait_timeout','50'),
('innodb_log_buffer_size','8388608'),
('innodb_log_checksums','ON'),
('innodb_log_compressed_pages','ON'),
('innodb_log_file_size','134217728'),
('innodb_log_files_in_group','2'),
('innodb_log_group_home_dir','/rdsdbdata/log/innodb'),
('innodb_log_spin_cpu_abs_lwm','80'),
('innodb_log_spin_cpu_pct_hwm','50'),
('innodb_log_wait_for_flush_spin_hwm','400'),
('innodb_log_write_ahead_size','8192'),
('innodb_log_writer_threads','ON'),
('innodb_lru_scan_depth','1024'),
('innodb_max_dirty_pages_pct','90.000000'),
('innodb_max_dirty_pages_pct_lwm','10.000000'),
('innodb_max_purge_lag','0'),
('innodb_max_purge_lag_delay','0'),
('innodb_max_undo_log_size','1073741824'),
('innodb_monitor_disable',''),
('innodb_monitor_enable',''),
('innodb_monitor_reset',''),
('innodb_monitor_reset_all',''),
('innodb_numa_interleave','OFF'),
('innodb_old_blocks_pct','37'),
('innodb_old_blocks_time','1000'),
('innodb_online_alter_log_max_size','134217728'),
('innodb_open_files','4000'),
('innodb_optimize_fulltext_only','OFF'),
('innodb_page_cleaners','1'),
('innodb_page_size','16384'),
('innodb_parallel_read_threads','4'),
('innodb_print_all_deadlocks','OFF'),
('innodb_print_ddl_logs','OFF'),
('innodb_purge_batch_size','300'),
('innodb_purge_rseg_truncate_frequency','128'),
('innodb_purge_threads','1'),
('innodb_random_read_ahead','OFF'),
('innodb_read_ahead_threshold','56'),
('innodb_read_io_threads','4'),
('innodb_read_only','OFF'),
('innodb_redo_log_archive_dirs',''),
('innodb_redo_log_capacity','2147483648'),
('innodb_redo_log_encrypt','OFF'),
('innodb_replication_delay','0'),
('innodb_rollback_on_timeout','OFF'),
('innodb_rollback_segments','128'),
('innodb_segment_reserve_factor','12.500000'),
('innodb_sort_buffer_size','1048576'),
('innodb_spin_wait_delay','6'),
('innodb_spin_wait_pause_multiplier','50'),
('innodb_stats_auto_recalc','ON'),
('innodb_stats_include_delete_marked','OFF'),
('innodb_stats_method','nulls_equal'),
('innodb_stats_on_metadata','OFF'),
('innodb_stats_persistent','ON'),
('innodb_stats_persistent_sample_pages','20'),
('innodb_stats_transient_sample_pages','8'),
('innodb_status_output','OFF'),
('innodb_status_output_locks','OFF'),
('innodb_strict_mode','ON'),
('innodb_sync_array_size','1'),
('innodb_sync_spin_loops','30'),
('innodb_table_locks','ON'),
('innodb_temp_data_file_path','ibtmp1:12M:autoextend'),
('innodb_temp_tablespaces_dir','./#innodb_temp/'),
('innodb_thread_concurrency','0'),
('innodb_thread_sleep_delay','10000'),
('innodb_tmpdir',''),
('innodb_undo_directory','./'),
('innodb_undo_log_encrypt','OFF'),
('innodb_undo_log_truncate','ON'),
('innodb_undo_tablespaces','2'),
('innodb_use_fdatasync','ON'),
('innodb_use_native_aio','ON'),
('innodb_validate_tablespace_paths','ON'),
('innodb_version','8.0.41'),
('innodb_write_io_threads','4'),
('interactive_timeout','28800'),
('internal_tmp_mem_storage_engine','TempTable'),
('join_buffer_size','262144'),
('keep_files_on_create','OFF'),
('key_buffer_size','16777216'),
('key_cache_age_threshold','300'),
('key_cache_block_size','1024'),
('key_cache_division_limit','100'),
('keyring_operations','ON'),
('large_files_support','ON'),
('large_page_size','0'),
('large_pages','OFF'),
('lc_messages','en_US'),
('lc_messages_dir','/rdsdbbin/mysql-8.0.41.R2/share/'),
('lc_time_names','en_US'),
('license','GPL'),
('local_infile','ON'),
('lock_wait_timeout','31536000'),
('locked_in_memory','OFF'),
('log_bin','OFF'),
('log_bin_basename',''),
('log_bin_index',''),
('log_bin_trust_function_creators','OFF'),
('log_bin_use_v1_row_events','OFF'),
('log_error','/rdsdbdata/log/error/mysql-error.log'),
('log_error_services','log_filter_internal; log_sink_internal'),
('log_error_suppression_list','MY-013360'),
('log_error_verbosity','2'),
('log_output','TABLE'),
('log_queries_not_using_indexes','OFF'),
('log_raw','OFF'),
('log_replica_updates','ON'),
('log_slave_updates','ON'),
('log_slow_admin_statements','OFF'),
('log_slow_extra','OFF'),
('log_slow_replica_statements','OFF'),
('log_slow_slave_statements','OFF'),
('log_statements_unsafe_for_binlog','OFF'),
('log_throttle_queries_not_using_indexes','0'),
('log_timestamps','UTC'),
('long_query_time','10.000000'),
('low_priority_updates','OFF'),
('lower_case_file_system','OFF'),
('lower_case_table_names','0'),
('mandatory_roles',''),
('master_info_repository','TABLE'),
('master_verify_checksum','OFF'),
('max_allowed_packet','67108864'),
('max_binlog_cache_size','18446744073709547520'),
('max_binlog_size','134217728'),
('max_binlog_stmt_cache_size','18446744073709547520'),
('max_connect_errors','100'),
('max_connections','60'),
('max_delayed_threads','20'),
('max_digest_length','1024'),
('max_error_count','1024'),
('max_execution_time','0'),
('max_heap_table_size','16777216'),
('max_insert_delayed_threads','20'),
('max_join_size','18446744073709551615'),
('max_length_for_sort_data','4096'),
('max_points_in_geometry','65536'),
('max_prepared_stmt_count','16382'),
('max_relay_log_size','0'),
('max_seeks_for_key','18446744073709551615'),
('max_sort_length','1024'),
('max_sp_recursion_depth','0'),
('max_user_connections','0'),
('max_write_lock_count','18446744073709551615'),
('min_examined_row_limit','0'),
('myisam_data_pointer_size','6'),
('myisam_max_sort_file_size','9223372036853727232'),
('myisam_mmap_size','18446744073709551615'),
('myisam_recover_options','OFF'),
('myisam_sort_buffer_size','8388608'),
('myisam_stats_method','nulls_unequal'),
('myisam_use_mmap','OFF'),
('mysql_native_password_proxy_users','OFF'),
('net_buffer_length','16384'),
('net_read_timeout','30'),
('net_retry_count','10'),
('net_write_timeout','60'),
('new','OFF'),
('ngram_token_size','2'),
('offline_mode','OFF'),
('old','OFF'),
('old_alter_table','OFF'),
('open_files_limit','1048576'),
('optimizer_max_subgraph_pairs','100000'),
('optimizer_prune_level','1'),
('optimizer_search_depth','62'),
('optimizer_switch','index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=on,hypergraph_optimizer=off,derived_condition_pushdown=on'),
('optimizer_trace','enabled=off,one_line=off'),
('optimizer_trace_features','greedy_search=on,range_optimizer=on,dynamic_range=on,repeated_subselect=on'),
('optimizer_trace_limit','1'),
('optimizer_trace_max_mem_size','1048576'),
('optimizer_trace_offset','-1'),
('parser_max_mem_size','18446744073709551615'),
('partial_revokes','OFF'),
('password_history','0'),
('password_require_current','OFF'),
('password_reuse_interval','0'),
('performance_schema','OFF'),
('performance_schema_accounts_size','0'),
('performance_schema_digests_size','0'),
('performance_schema_error_size','0'),
('performance_schema_events_stages_history_long_size','0'),
('performance_schema_events_stages_history_size','0'),
('performance_schema_events_statements_history_long_size','0'),
('performance_schema_events_statements_history_size','0'),
('performance_schema_events_transactions_history_long_size','0'),
('performance_schema_events_transactions_history_size','0'),
('performance_schema_events_waits_history_long_size','0'),
('performance_schema_events_waits_history_size','0'),
('performance_schema_hosts_size','0'),
('performance_schema_max_cond_classes','0'),
('performance_schema_max_cond_instances','0'),
('performance_schema_max_digest_length','0'),
('performance_schema_max_digest_sample_age','60'),
('performance_schema_max_file_classes','0'),
('performance_schema_max_file_handles','0'),
('performance_schema_max_file_instances','0'),
('performance_schema_max_index_stat','0'),
('performance_schema_max_memory_classes','0'),
('performance_schema_max_metadata_locks','0'),
('performance_schema_max_mutex_classes','0'),
('performance_schema_max_mutex_instances','0'),
('performance_schema_max_prepared_statements_instances','0'),
('performance_schema_max_program_instances','0'),
('performance_schema_max_rwlock_classes','0'),
('performance_schema_max_rwlock_instances','0'),
('performance_schema_max_socket_classes','0'),
('performance_schema_max_socket_instances','0'),
('performance_schema_max_sql_text_length','0'),
('performance_schema_max_stage_classes','0'),
('performance_schema_max_statement_classes','0'),
('performance_schema_max_statement_stack','0'),
('performance_schema_max_table_handles','0'),
('performance_schema_max_table_instances','0'),
('performance_schema_max_table_lock_stat','0'),
('performance_schema_max_thread_classes','0'),
('performance_schema_max_thread_instances','0'),
('performance_schema_session_connect_attrs_size','0'),
('performance_schema_setup_actors_size','0'),
('performance_schema_setup_objects_size','0'),
('performance_schema_show_processlist','OFF'),
('performance_schema_users_size','0'),
('persist_only_admin_x509_subject',''),
('persist_sensitive_variables_in_plaintext','ON'),
('persisted_globals_load','OFF'),
('pid_file','/rdsdbdata/log/mysql-3306.pid'),
('plugin_dir','/rdsdbbin/mysql-8.0.41.R2/lib/plugin/'),
('port','3306'),
('preload_buffer_size','32768'),
('print_identified_with_as_hex','OFF'),
('profiling','OFF'),
('profiling_history_size','15'),
('protocol_compression_algorithms','zlib,zstd,uncompressed'),
('protocol_version','10'),
('query_alloc_block_size','8192'),
('query_prealloc_size','8192'),
('range_alloc_block_size','4096'),
('range_optimizer_max_mem_size','8388608'),
('rbr_exec_mode','STRICT'),
('read_buffer_size','262144'),
('read_only','OFF'),
('read_rnd_buffer_size','524288'),
('regexp_stack_limit','8000000'),
('regexp_time_limit','32'),
('relay_log','/rdsdbdata/log/relaylog/relaylog'),
('relay_log_basename','/rdsdbdata/log/relaylog/relaylog'),
('relay_log_index','/rdsdbdata/log/relaylog/relaylog.index'),
('relay_log_info_file','relay-log.info'),
('relay_log_info_repository','TABLE'),
('relay_log_purge','ON'),
('relay_log_recovery','ON'),
('relay_log_space_limit','0'),
('replica_allow_batching','ON'),
('replica_checkpoint_group','512'),
('replica_checkpoint_period','300'),
('replica_compressed_protocol','OFF'),
('replica_exec_mode','IDEMPOTENT'),
('replica_load_tmpdir','/rdsdbdata/tmp'),
('replica_max_allowed_packet','1073741824'),
('replica_net_timeout','60'),
('replica_parallel_type','LOGICAL_CLOCK'),
('replica_parallel_workers','4'),
('replica_pending_jobs_size_max','134217728'),
('replica_preserve_commit_order','ON'),
('replica_skip_errors','OFF'),
('replica_sql_verify_checksum','ON'),
('replica_transaction_retries','10'),
('replica_type_conversions',''),
('replication_optimize_for_static_plugin_config','OFF'),
('replication_sender_observe_commit_only','OFF'),
('report_host',''),
('report_password',''),
('report_port','3306'),
('report_user',''),
('require_secure_transport','OFF'),
('rpl_read_size','8192'),
('rpl_stop_replica_timeout','31536000'),
('rpl_stop_slave_timeout','31536000'),
('schema_definition_cache','256'),
('secondary_engine_cost_threshold','100000.000000'),
('secure_file_priv','/secure_file_priv_dir/'),
('select_into_buffer_size','131072'),
('select_into_disk_sync','OFF'),
('select_into_disk_sync_delay','0'),
('server_id','1806218587'),
('server_id_bits','32'),
('server_uuid','a08bb40d-3d64-11f0-bc32-12ea7e1126d9'),
('session_track_gtids','OFF'),
('session_track_schema','ON'),
('session_track_state_change','OFF'),
('session_track_system_variables','time_zone,autocommit,character_set_client,character_set_results,character_set_connection'),
('session_track_transaction_info','OFF'),
('sha256_password_auto_generate_rsa_keys','ON'),
('sha256_password_private_key_path','private_key.pem'),
('sha256_password_proxy_users','OFF'),
('sha256_password_public_key_path','public_key.pem'),
('show_create_table_verbosity','OFF'),
('show_gipk_in_create_table_and_information_schema','ON'),
('show_old_temporals','OFF'),
('skip_external_locking','ON'),
('skip_name_resolve','OFF'),
('skip_networking','OFF'),
('skip_replica_start','ON'),
('skip_show_database','OFF'),
('skip_slave_start','ON'),
('slave_allow_batching','ON'),
('slave_checkpoint_group','512'),
('slave_checkpoint_period','300'),
('slave_compressed_protocol','OFF'),
('slave_exec_mode','IDEMPOTENT'),
('slave_load_tmpdir','/rdsdbdata/tmp'),
('slave_max_allowed_packet','1073741824'),
('slave_net_timeout','60'),
('slave_parallel_type','LOGICAL_CLOCK'),
('slave_parallel_workers','4'),
('slave_pending_jobs_size_max','134217728'),
('slave_preserve_commit_order','ON'),
('slave_rows_search_algorithms','INDEX_SCAN,HASH_SCAN'),
('slave_skip_errors','OFF'),
('slave_sql_verify_checksum','ON'),
('slave_transaction_retries','10'),
('slave_type_conversions',''),
('slow_launch_time','2'),
('slow_query_log','OFF'),
('slow_query_log_file','/rdsdbdata/log/slowquery/mysql-slowquery.log'),
('socket','/tmp/mysql.sock'),
('sort_buffer_size','262144'),
('source_verify_checksum','OFF'),
('sql_auto_is_null','OFF'),
('sql_big_selects','ON'),
('sql_buffer_result','OFF'),
('sql_generate_invisible_primary_key','OFF'),
('sql_log_off','OFF'),
('sql_mode','NO_ENGINE_SUBSTITUTION'),
('sql_notes','ON'),
('sql_quote_show_create','ON'),
('sql_replica_skip_counter','0'),
('sql_require_primary_key','OFF'),
('sql_safe_updates','OFF'),
('sql_select_limit','18446744073709551615'),
('sql_slave_skip_counter','0'),
('sql_warnings','OFF'),
('ssl_ca','/rdsdbdata/rds-metadata/ca-cert.pem'),
('ssl_capath',''),
('ssl_cert','/rdsdbdata/rds-metadata/server-cert.pem'),
('ssl_cipher',''),
('ssl_crl',''),
('ssl_crlpath',''),
('ssl_fips_mode','OFF'),
('ssl_key','/rdsdbdata/rds-metadata/server-key.pem'),
('ssl_session_cache_mode','ON'),
('ssl_session_cache_timeout','300'),
('stored_program_cache','256'),
('stored_program_definition_cache','256'),
('super_read_only','OFF'),
('sync_binlog','1'),
('sync_master_info','10000'),
('sync_relay_log','10000'),
('sync_relay_log_info','10000'),
('sync_source_info','10000'),
('system_time_zone','UTC'),
('table_definition_cache','2000'),
('table_encryption_privilege_check','OFF'),
('table_open_cache','4000'),
('table_open_cache_instances','16'),
('tablespace_definition_cache','256'),
('temptable_max_mmap','1073741824'),
('temptable_max_ram','1073741824'),
('temptable_use_mmap','ON'),
('terminology_use_previous','BEFORE_8_0_26'),
('thread_cache_size','8'),
('thread_handling','one-thread-per-connection'),
('thread_stack','262144'),
('time_zone','UTC'),
('tls_ciphersuites',''),
('tls_version','TLSv1.2,TLSv1.3'),
('tmp_table_size','16777216'),
('tmpdir','/rdsdbdata/tmp'),
('transaction_alloc_block_size','8192'),
('transaction_isolation','REPEATABLE-READ'),
('transaction_prealloc_size','4096'),
('transaction_read_only','OFF'),
('transaction_write_set_extraction','XXHASH64'),
('unique_checks','ON'),
('updatable_views_with_limit','YES'),
('version','8.0.41'),
('version_comment','Source distribution'),
('version_compile_machine','aarch64'),
('version_compile_os','Linux'),
('version_compile_zlib','1.3.1'),
('wait_timeout','28800'),
('windowing_use_high_precision','ON'),
('xa_detach_on_prepare','ON');
/*!40000 ALTER TABLE `global_variables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_cache`
--

DROP TABLE IF EXISTS `host_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `host_cache` (
  `IP` varchar(64) NOT NULL,
  `HOST` varchar(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `HOST_VALIDATED` enum('YES','NO') NOT NULL,
  `SUM_CONNECT_ERRORS` bigint NOT NULL,
  `COUNT_HOST_BLOCKED_ERRORS` bigint NOT NULL,
  `COUNT_NAMEINFO_TRANSIENT_ERRORS` bigint NOT NULL,
  `COUNT_NAMEINFO_PERMANENT_ERRORS` bigint NOT NULL,
  `COUNT_FORMAT_ERRORS` bigint NOT NULL,
  `COUNT_ADDRINFO_TRANSIENT_ERRORS` bigint NOT NULL,
  `COUNT_ADDRINFO_PERMANENT_ERRORS` bigint NOT NULL,
  `COUNT_FCRDNS_ERRORS` bigint NOT NULL,
  `COUNT_HOST_ACL_ERRORS` bigint NOT NULL,
  `COUNT_NO_AUTH_PLUGIN_ERRORS` bigint NOT NULL,
  `COUNT_AUTH_PLUGIN_ERRORS` bigint NOT NULL,
  `COUNT_HANDSHAKE_ERRORS` bigint NOT NULL,
  `COUNT_PROXY_USER_ERRORS` bigint NOT NULL,
  `COUNT_PROXY_USER_ACL_ERRORS` bigint NOT NULL,
  `COUNT_AUTHENTICATION_ERRORS` bigint NOT NULL,
  `COUNT_SSL_ERRORS` bigint NOT NULL,
  `COUNT_MAX_USER_CONNECTIONS_ERRORS` bigint NOT NULL,
  `COUNT_MAX_USER_CONNECTIONS_PER_HOUR_ERRORS` bigint NOT NULL,
  `COUNT_DEFAULT_DATABASE_ERRORS` bigint NOT NULL,
  `COUNT_INIT_CONNECT_ERRORS` bigint NOT NULL,
  `COUNT_LOCAL_ERRORS` bigint NOT NULL,
  `COUNT_UNKNOWN_ERRORS` bigint NOT NULL,
  `FIRST_SEEN` timestamp NOT NULL,
  `LAST_SEEN` timestamp NOT NULL,
  `FIRST_ERROR_SEEN` timestamp NULL DEFAULT NULL,
  `LAST_ERROR_SEEN` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`IP`),
  KEY `HOST` (`HOST`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_cache`
--

LOCK TABLES `host_cache` WRITE;
/*!40000 ALTER TABLE `host_cache` DISABLE KEYS */;
INSERT INTO `host_cache` VALUES
('223.233.83.46',NULL,'YES',0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'2025-06-14 07:32:44','2025-06-14 07:51:34','2025-06-14 07:32:44','2025-06-14 07:32:44'),
('74.82.47.33','scan-12f.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-13 19:24:11','2025-06-13 19:24:11','2025-06-13 19:24:12','2025-06-13 19:24:12'),
('18.188.53.152','ec2-18-188-53-152.us-east-2.compute.amazonaws.com','YES',2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-12 23:02:51','2025-06-13 18:32:13','2025-06-12 23:02:51','2025-06-13 18:32:14'),
('45.91.171.220',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-04 15:31:43','2025-06-13 14:49:52','2025-06-04 15:31:43','2025-06-13 14:49:52'),
('113.30.150.132',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-11 17:42:37','2025-06-13 13:22:51','2025-06-11 17:42:37','2025-06-13 13:22:51'),
('135.237.125.156','azpdes4naqft.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-13 00:36:27','2025-06-13 00:36:27','2025-06-13 00:36:27','2025-06-13 00:36:27'),
('34.38.2.214',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-13 00:05:01','2025-06-13 00:05:01','2025-06-13 00:05:01','2025-06-13 00:05:02'),
('116.68.160.146',NULL,'YES',1,0,0,1,0,0,0,0,0,0,151,1,0,0,0,0,0,0,0,0,0,0,'2025-06-12 21:50:57','2025-06-12 21:54:13','2025-06-12 21:50:57','2025-06-12 21:54:14'),
('205.210.31.175',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-12 21:52:42','2025-06-12 21:52:42','2025-06-12 21:52:42','2025-06-12 21:52:42'),
('38.196.246.150',NULL,'YES',1,0,0,1,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-12 21:30:06','2025-06-12 21:30:17','2025-06-12 21:30:06','2025-06-12 21:30:17'),
('64.227.111.1',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-12 20:16:28','2025-06-12 20:16:28','2025-06-12 20:16:28','2025-06-12 20:16:28'),
('106.75.137.178',NULL,'YES',0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,'2025-06-12 17:58:02','2025-06-12 17:58:02','2025-06-12 17:58:02','2025-06-12 17:58:02'),
('167.94.138.162',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-12 17:23:41','2025-06-12 17:24:10','2025-06-12 17:23:41','2025-06-12 17:24:11'),
('104.234.115.218','crawler218.deepfield.net','YES',3,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,'2025-06-12 15:04:45','2025-06-12 15:05:13','2025-06-12 15:04:55','2025-06-12 15:05:14'),
('139.144.52.241','139-144-52-241.ip.linodeusercontent.com','YES',51,0,0,0,0,0,0,0,0,0,0,51,0,0,0,0,0,0,0,0,0,0,'2025-06-12 14:57:03','2025-06-12 14:57:16','2025-06-12 14:57:03','2025-06-12 14:57:16'),
('205.210.31.224',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-12 14:32:39','2025-06-12 14:32:39','2025-06-12 14:32:39','2025-06-12 14:32:39'),
('78.44.164.150','ip-78-44-164-150.bb.vodafone.cz','YES',1,0,0,0,0,0,0,0,0,0,2,1,0,0,149,0,0,0,0,0,0,0,'2025-06-12 14:00:14','2025-06-12 14:01:00','2025-06-12 14:00:14','2025-06-12 14:01:00'),
('3.23.104.96','ec2-3-23-104-96.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-12 13:35:13','2025-06-12 13:35:13','2025-06-12 13:35:13','2025-06-12 13:35:13'),
('20.221.66.246','azpdcgvken3s.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-12 09:46:59','2025-06-12 09:46:59','2025-06-12 09:46:59','2025-06-12 09:46:59'),
('152.32.141.199',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-12 06:54:24','2025-06-12 06:54:26','2025-06-12 06:54:24','2025-06-12 06:54:26'),
('159.196.9.241',NULL,'YES',1,0,0,0,0,0,2,0,0,0,117,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 21:13:33','2025-06-11 21:15:41','2025-06-11 21:13:33','2025-06-11 21:15:42'),
('20.65.193.198','azpdssw7f4ws.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 20:50:15','2025-06-11 20:50:15','2025-06-11 20:50:15','2025-06-11 20:50:15'),
('20.55.90.128','azpdesqxxz9d.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 20:20:08','2025-06-11 20:20:08','2025-06-11 20:20:09','2025-06-11 20:20:09'),
('18.224.93.149','ec2-18-224-93-149.us-east-2.compute.amazonaws.com','YES',2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-02 12:16:46','2025-06-11 20:06:34','2025-06-02 12:16:47','2025-06-11 20:06:34'),
('65.49.20.122','scan-17n.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 17:17:50','2025-06-11 17:17:50','2025-06-11 17:17:50','2025-06-11 17:17:50'),
('9.234.10.182','azpdcswz4pa4.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 16:05:25','2025-06-11 16:05:25','2025-06-11 16:05:25','2025-06-11 16:05:25'),
('134.122.30.157',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 15:52:50','2025-06-11 15:52:50','2025-06-11 15:52:50','2025-06-11 15:52:50'),
('35.224.176.50',NULL,'NO',0,0,0,0,397,0,0,0,0,0,0,0,0,0,397,0,0,0,0,0,0,0,'2025-06-11 12:25:49','2025-06-11 12:27:24','2025-06-11 12:25:49','2025-06-11 12:27:24'),
('47.84.177.166',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 11:41:44','2025-06-11 11:41:44','2025-06-11 11:41:44','2025-06-11 11:41:44'),
('15.235.189.158','gardner.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 07:09:28','2025-06-11 07:09:28','2025-06-11 07:09:31','2025-06-11 07:09:31'),
('15.235.189.148','antonio.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 07:09:27','2025-06-11 07:09:27','2025-06-11 07:09:28','2025-06-11 07:09:28'),
('15.235.189.153','anton.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 07:08:36','2025-06-11 07:08:36','2025-06-11 07:08:46','2025-06-11 07:08:46'),
('15.235.189.156','noble.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 07:08:31','2025-06-11 07:08:31','2025-06-11 07:08:35','2025-06-11 07:08:35'),
('71.6.199.87',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 05:02:13','2025-06-11 05:02:13','2025-06-11 05:02:13','2025-06-11 05:02:13'),
('20.168.0.84',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-11 00:58:24','2025-06-11 00:58:24','2025-06-11 00:58:24','2025-06-11 00:58:24'),
('167.94.138.192',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-10 22:52:50','2025-06-10 22:53:06','2025-06-10 22:52:50','2025-06-10 22:53:06'),
('20.169.83.190','azpdwsayb3a2.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 20:23:14','2025-06-10 20:23:14','2025-06-10 20:23:14','2025-06-10 20:23:14'),
('65.49.20.93','scan-20f.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 17:57:02','2025-06-10 17:57:02','2025-06-10 17:57:02','2025-06-10 17:57:02'),
('205.210.31.40',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 16:19:12','2025-06-10 16:19:12','2025-06-10 16:19:12','2025-06-10 16:19:22'),
('18.222.192.238','ec2-18-222-192-238.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 14:56:08','2025-06-10 14:56:08','2025-06-10 14:56:08','2025-06-10 14:56:08'),
('38.171.255.69',NULL,'YES',2,0,0,1,0,0,0,0,0,0,2,2,0,0,96,0,0,0,0,0,0,0,'2025-06-02 13:46:23','2025-06-10 13:51:33','2025-06-02 13:46:23','2025-06-10 13:51:33'),
('185.247.137.89','deliberate.monitoring.internet-measurement.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 13:08:42','2025-06-10 13:08:42','2025-06-10 13:08:44','2025-06-10 13:08:44'),
('47.236.79.236',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 11:29:37','2025-06-10 11:29:37','2025-06-10 11:29:37','2025-06-10 11:29:38'),
('134.122.106.248',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 07:52:45','2025-06-10 07:52:45','2025-06-10 07:52:45','2025-06-10 07:52:45'),
('121.228.41.44',NULL,'YES',0,0,0,19,0,0,0,0,0,0,0,0,0,0,98,0,0,0,0,0,0,0,'2025-06-03 05:57:14','2025-06-10 06:58:07','2025-06-03 05:57:14','2025-06-10 06:58:08'),
('156.229.16.142',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,'2025-06-10 06:36:23','2025-06-10 06:36:41','2025-06-10 06:36:23','2025-06-10 06:36:41'),
('161.35.186.21',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-10 06:30:45','2025-06-10 06:30:45','2025-06-10 06:30:45','2025-06-10 06:30:45'),
('113.30.150.23',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-05-31 16:39:37','2025-06-10 05:04:44','2025-05-31 16:39:37','2025-06-10 05:04:44'),
('137.184.33.181',NULL,'YES',1,0,0,1,0,0,0,0,0,0,2,1,0,0,115,0,0,0,0,0,0,0,'2025-06-10 04:50:43','2025-06-10 04:51:10','2025-06-10 04:50:43','2025-06-10 04:51:11'),
('45.147.250.208',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 04:34:44','2025-06-10 04:34:44','2025-06-10 04:34:44','2025-06-10 04:34:44'),
('113.30.151.61',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 04:31:48','2025-06-10 04:31:48','2025-06-10 04:31:48','2025-06-10 04:31:48'),
('71.6.232.27',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 03:44:41','2025-06-10 03:44:41','2025-06-10 03:44:41','2025-06-10 03:44:49'),
('3.144.120.21','ec2-3-144-120-21.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 03:33:06','2025-06-10 03:33:06','2025-06-10 03:33:06','2025-06-10 03:33:06'),
('91.223.169.83',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 03:23:03','2025-06-10 03:23:03','2025-06-10 03:23:03','2025-06-10 03:23:03'),
('185.47.172.136',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 02:41:39','2025-06-10 02:41:39','2025-06-10 02:41:39','2025-06-10 02:41:39'),
('45.147.250.222',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-10 00:02:11','2025-06-10 00:02:11','2025-06-10 00:02:11','2025-06-10 00:02:11'),
('167.94.138.167',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-09 23:12:39','2025-06-09 23:12:58','2025-06-09 23:12:39','2025-06-09 23:12:59'),
('20.12.240.9','azpdcse025j0.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 19:52:58','2025-06-09 19:52:58','2025-06-09 19:52:58','2025-06-09 19:52:58'),
('223.233.83.244',NULL,'YES',0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'2025-06-09 07:55:59','2025-06-09 17:21:50','2025-06-09 07:55:59','2025-06-09 07:55:59'),
('205.210.31.173',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 16:28:42','2025-06-09 16:28:42','2025-06-09 16:28:42','2025-06-09 16:28:52'),
('14.47.38.214',NULL,'YES',1,0,0,2,0,0,0,0,0,0,2,1,0,0,115,0,0,0,0,0,0,0,'2025-06-09 15:04:21','2025-06-09 15:05:29','2025-06-09 15:04:21','2025-06-09 15:05:29'),
('206.0.165.151',NULL,'YES',1,0,0,1,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-09 14:25:12','2025-06-09 14:25:23','2025-06-09 14:25:12','2025-06-09 14:25:23'),
('45.156.128.97','sh-ams-nl-gp1-wk142b.internet-census.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 14:23:01','2025-06-09 14:23:01','2025-06-09 14:23:02','2025-06-09 14:23:02'),
('66.228.53.157','66-228-53-157.ip.linodeusercontent.com','YES',2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-09 14:20:41','2025-06-09 14:20:41','2025-06-09 14:20:41','2025-06-09 14:20:41'),
('104.234.115.80','crawler080.deepfield.net','YES',3,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,'2025-06-09 13:56:21','2025-06-09 13:56:44','2025-06-09 13:56:31','2025-06-09 13:56:44'),
('40.124.186.157','azpdsgrxj5h2.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 11:44:55','2025-06-09 11:44:55','2025-06-09 11:44:55','2025-06-09 11:44:55'),
('81.29.134.51',NULL,'YES',2,0,0,0,0,0,1,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,'2025-06-09 10:08:28','2025-06-09 10:08:29','2025-06-09 10:08:28','2025-06-09 10:08:29'),
('138.199.60.7',NULL,'YES',0,0,0,1,0,0,0,0,0,0,3,0,0,0,2,0,0,0,0,0,0,0,'2025-06-09 07:09:19','2025-06-09 07:09:25','2025-06-09 07:09:19','2025-06-09 07:09:26'),
('199.45.154.151',NULL,'YES',5,0,0,0,0,0,1,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-09 06:51:42','2025-06-09 06:51:53','2025-06-09 06:51:42','2025-06-09 06:51:54'),
('198.235.24.6',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 05:13:06','2025-06-09 05:13:06','2025-06-09 05:13:06','2025-06-09 05:13:06'),
('18.191.255.164','ec2-18-191-255-164.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-09 02:29:48','2025-06-09 02:29:48','2025-06-09 02:29:49','2025-06-09 02:29:49'),
('60.190.226.189',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 23:32:44','2025-06-08 23:32:44','2025-06-08 23:32:44','2025-06-08 23:32:54'),
('111.113.89.69',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 23:05:27','2025-06-08 23:05:27','2025-06-08 23:05:27','2025-06-08 23:05:27'),
('34.140.38.148',NULL,'NO',0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,'2025-06-08 22:31:47','2025-06-08 22:31:47','2025-06-08 22:31:47','2025-06-08 22:31:47'),
('34.140.32.240',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 22:31:46','2025-06-08 22:31:46','2025-06-08 22:31:46','2025-06-08 22:31:47'),
('143.244.182.6',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-08 18:59:01','2025-06-08 18:59:01','2025-06-08 18:59:01','2025-06-08 18:59:01'),
('106.75.164.40',NULL,'YES',0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,'2025-06-08 17:55:48','2025-06-08 17:55:48','2025-06-08 17:55:48','2025-06-08 17:55:48'),
('198.235.24.134',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 16:51:57','2025-06-08 16:51:57','2025-06-08 16:51:57','2025-06-08 16:52:07'),
('20.65.195.51','azpdss37d5iu.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 16:24:16','2025-06-08 16:24:16','2025-06-08 16:24:16','2025-06-08 16:24:16'),
('18.119.13.69','ec2-18-119-13-69.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 15:44:13','2025-06-08 15:44:13','2025-06-08 15:44:13','2025-06-08 15:44:13'),
('20.127.202.110','azpdes6uvmgf.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 12:54:20','2025-06-08 12:54:20','2025-06-08 12:54:20','2025-06-08 12:54:20'),
('77.53.236.193','h77-53-236-193.cust.bredband2.com','YES',1,0,0,0,0,0,0,0,0,0,117,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 12:11:30','2025-06-08 12:12:28','2025-06-08 12:11:30','2025-06-08 12:12:28'),
('8.208.10.94',NULL,'YES',1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 07:35:00','2025-06-08 07:35:00','2025-06-08 07:35:00','2025-06-08 07:35:01'),
('206.168.34.79',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-08 05:21:51','2025-06-08 05:22:14','2025-06-08 05:21:51','2025-06-08 05:22:14'),
('152.32.150.117',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 04:40:51','2025-06-08 04:40:51','2025-06-08 04:40:51','2025-06-08 04:40:51'),
('18.191.173.38','ec2-18-191-173-38.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 02:10:51','2025-06-08 02:10:51','2025-06-08 02:10:52','2025-06-08 02:10:52'),
('146.190.41.214',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 01:47:57','2025-06-08 01:47:57','2025-06-08 01:47:57','2025-06-08 01:47:57'),
('91.196.152.43','andersen.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 00:28:47','2025-06-08 00:28:47','2025-06-08 00:28:50','2025-06-08 00:28:50'),
('91.196.152.67','stephen.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 00:28:47','2025-06-08 00:28:47','2025-06-08 00:28:47','2025-06-08 00:28:47'),
('91.196.152.40','adeel.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 00:28:25','2025-06-08 00:28:25','2025-06-08 00:28:35','2025-06-08 00:28:35'),
('91.196.152.46','cairo.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-08 00:28:24','2025-06-08 00:28:24','2025-06-08 00:28:25','2025-06-08 00:28:25'),
('108.176.102.58','syn-108-176-102-058.biz.spectrum.com','YES',0,0,0,0,0,0,0,0,0,0,0,0,0,0,397,0,0,0,0,0,0,0,'2025-06-07 23:22:19','2025-06-07 23:23:54','2025-06-07 23:22:19','2025-06-07 23:23:54'),
('87.236.176.114','lovely.monitoring.internet-measurement.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-07 18:47:09','2025-06-07 18:47:09','2025-06-07 18:47:10','2025-06-07 18:47:10'),
('205.210.31.182',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-07 15:47:53','2025-06-07 15:47:53','2025-06-07 15:47:53','2025-06-07 15:48:03'),
('38.188.238.201',NULL,'YES',3,0,0,1,0,0,0,0,0,0,3,3,0,0,144,0,0,0,0,0,0,0,'2025-06-01 16:58:49','2025-06-07 14:44:12','2025-06-01 16:58:49','2025-06-07 14:44:12'),
('20.65.192.71','azpdssxxiv0f.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-07 11:47:03','2025-06-07 11:47:03','2025-06-07 11:47:03','2025-06-07 11:47:03'),
('148.113.210.254','a3.scanner.modat.io','YES',24,0,0,0,0,0,0,0,0,0,0,24,0,0,0,0,0,0,0,0,0,0,'2025-06-07 06:54:25','2025-06-07 06:56:21','2025-06-07 06:54:25','2025-06-07 06:56:21'),
('52.15.76.227','ec2-52-15-76-227.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-07 02:33:26','2025-06-07 02:33:26','2025-06-07 02:33:27','2025-06-07 02:33:27'),
('164.52.24.182',NULL,'YES',3,0,0,2,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,'2025-06-07 01:48:50','2025-06-07 01:48:53','2025-06-07 01:48:50','2025-06-07 01:48:53'),
('45.131.155.254',NULL,'YES',7,0,0,1,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,'2025-05-30 20:45:07','2025-06-06 20:41:11','2025-05-30 20:45:07','2025-06-06 20:41:11'),
('206.168.34.121',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-06 16:01:24','2025-06-06 16:01:59','2025-06-06 16:01:24','2025-06-06 16:02:01'),
('205.210.31.96',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 15:59:38','2025-06-06 15:59:38','2025-06-06 15:59:38','2025-06-06 15:59:48'),
('38.25.159.125',NULL,'YES',1,0,0,1,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-06 15:01:33','2025-06-06 15:01:42','2025-06-06 15:01:33','2025-06-06 15:01:42'),
('20.83.167.20','azpdegwtnous.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 11:37:23','2025-06-06 11:37:23','2025-06-06 11:37:23','2025-06-06 11:37:23'),
('20.168.13.44','azpdws8wcrwj.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 10:28:06','2025-06-06 10:28:06','2025-06-06 10:28:07','2025-06-06 10:28:07'),
('64.62.197.241','scan-51o.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 09:23:49','2025-06-06 09:23:49','2025-06-06 09:23:49','2025-06-06 09:23:49'),
('3.142.219.55','ec2-3-142-219-55.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 07:34:59','2025-06-06 07:34:59','2025-06-06 07:35:00','2025-06-06 07:35:00'),
('58.212.237.213',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 06:39:34','2025-06-06 06:39:34','2025-06-06 06:39:34','2025-06-06 06:39:35'),
('91.196.152.210','taliah.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 00:05:08','2025-06-06 00:05:08','2025-06-06 00:05:11','2025-06-06 00:05:11'),
('91.196.152.209','edith.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 00:05:08','2025-06-06 00:05:08','2025-06-06 00:05:08','2025-06-06 00:05:08'),
('91.196.152.211','holmes.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 00:04:27','2025-06-06 00:04:27','2025-06-06 00:04:37','2025-06-06 00:04:37'),
('91.196.152.179','kier.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-06 00:04:27','2025-06-06 00:04:27','2025-06-06 00:04:27','2025-06-06 00:04:27'),
('185.77.218.11',NULL,'YES',0,0,0,1,0,0,0,0,0,0,3,0,0,0,2,0,0,0,0,0,0,0,'2025-06-05 18:59:08','2025-06-05 18:59:10','2025-06-05 18:59:08','2025-06-05 18:59:11'),
('223.233.82.33',NULL,'YES',0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'2025-06-05 17:43:08','2025-06-05 17:44:03','2025-06-05 17:43:08','2025-06-05 17:43:08'),
('38.52.141.108',NULL,'YES',1,0,0,1,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-05 15:49:46','2025-06-05 15:50:18','2025-06-05 15:49:46','2025-06-05 15:50:19'),
('205.210.31.228',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-05 15:13:42','2025-06-05 15:13:42','2025-06-05 15:13:42','2025-06-05 15:13:52'),
('18.219.193.156','ec2-18-219-193-156.us-east-2.compute.amazonaws.com','YES',2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-03 17:49:43','2025-06-05 10:24:04','2025-06-03 17:49:43','2025-06-05 10:24:04'),
('167.71.3.188',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-05 09:10:36','2025-06-05 09:10:36','2025-06-05 09:10:36','2025-06-05 09:10:36'),
('20.65.193.148','azpdss8gaq8b.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-05 08:27:38','2025-06-05 08:27:38','2025-06-05 08:27:38','2025-06-05 08:27:38'),
('223.233.87.200',NULL,'YES',0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,'2025-06-02 07:14:17','2025-06-05 07:28:19','2025-06-02 07:14:17','2025-06-04 14:01:14'),
('199.45.155.91',NULL,'YES',5,0,0,0,0,0,1,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-05 07:00:46','2025-06-05 07:01:05','2025-06-05 07:00:46','2025-06-05 07:01:05'),
('20.15.200.100','azpdcs981gn1.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-05 06:42:37','2025-06-05 06:42:37','2025-06-05 06:42:37','2025-06-05 06:42:37'),
('206.1.154.183',NULL,'YES',1,0,0,2,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-05 05:24:31','2025-06-05 05:24:39','2025-06-05 05:24:31','2025-06-05 05:24:39'),
('52.165.80.210','azpdcgqawif3.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-05 02:58:36','2025-06-05 02:58:36','2025-06-05 02:58:36','2025-06-05 02:58:36'),
('167.94.138.174',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-05 02:46:36','2025-06-05 02:46:57','2025-06-05 02:46:36','2025-06-05 02:46:58'),
('34.77.65.25',NULL,'NO',0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,'2025-06-05 02:35:41','2025-06-05 02:35:41','2025-06-05 02:35:41','2025-06-05 02:35:41'),
('34.77.21.148',NULL,'NO',0,0,0,0,2,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 01:18:53','2025-06-05 02:35:41','2025-06-03 01:18:53','2025-06-05 02:35:41'),
('44.220.188.3','ec2-44-220-188-3.compute-1.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 21:59:56','2025-06-04 21:59:56','2025-06-04 21:59:56','2025-06-04 21:59:56'),
('64.62.197.72','scan-38k.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 18:37:06','2025-06-04 18:37:06','2025-06-04 18:37:07','2025-06-04 18:37:07'),
('18.218.94.172','ec2-18-218-94-172.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 16:35:44','2025-06-04 16:35:44','2025-06-04 16:35:45','2025-06-04 16:35:45'),
('205.210.31.64',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 15:07:05','2025-06-04 15:07:05','2025-06-04 15:07:05','2025-06-04 15:07:15'),
('38.41.8.81',NULL,'NO',0,0,0,0,50,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-04 14:18:31','2025-06-04 14:18:41','2025-06-04 14:18:31','2025-06-04 14:18:41'),
('34.79.208.213',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 11:44:03','2025-06-04 11:44:03','2025-06-04 11:44:03','2025-06-04 11:44:03'),
('195.184.76.129','aleksander.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 11:25:52','2025-06-04 11:25:52','2025-06-04 11:25:55','2025-06-04 11:25:55'),
('195.184.76.132','brooks.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 11:25:52','2025-06-04 11:25:52','2025-06-04 11:25:52','2025-06-04 11:25:52'),
('195.184.76.88','barnett.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 11:21:54','2025-06-04 11:21:54','2025-06-04 11:22:04','2025-06-04 11:22:04'),
('195.184.76.93','larry.probe.onyphe.net','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 11:21:54','2025-06-04 11:21:54','2025-06-04 11:21:54','2025-06-04 11:21:54'),
('71.6.199.65',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 09:20:53','2025-06-04 09:20:53','2025-06-04 09:20:53','2025-06-04 09:20:54'),
('18.221.214.151','ec2-18-221-214-151.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-04 08:52:53','2025-06-04 08:52:53','2025-06-04 08:52:53','2025-06-04 08:52:53'),
('173.197.14.226','syn-173-197-014-226.biz.spectrum.com','YES',0,0,0,0,0,0,0,0,0,0,0,0,0,0,397,0,0,0,0,0,0,0,'2025-06-03 22:55:37','2025-06-03 22:57:13','2025-06-03 22:55:37','2025-06-03 22:57:13'),
('135.237.125.135','azpdeso9n9of.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 22:22:47','2025-06-03 22:22:47','2025-06-03 22:22:47','2025-06-03 22:22:47'),
('162.142.125.119',NULL,'YES',5,0,0,0,0,0,1,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-03 19:11:17','2025-06-03 19:11:54','2025-06-03 19:11:17','2025-06-03 19:11:54'),
('20.29.23.140','azpdcgdr5l3k.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 19:07:01','2025-06-03 19:07:01','2025-06-03 19:07:01','2025-06-03 19:07:01'),
('71.6.232.26',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 17:06:47','2025-06-03 17:06:47','2025-06-03 17:06:47','2025-06-03 17:06:54'),
('205.210.31.250',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 15:51:46','2025-06-03 15:51:46','2025-06-03 15:51:46','2025-06-03 15:51:56'),
('38.51.120.12',NULL,'YES',1,0,0,1,0,0,0,0,0,0,1,1,0,0,48,0,0,0,0,0,0,0,'2025-06-03 12:34:02','2025-06-03 12:34:41','2025-06-03 12:34:02','2025-06-03 12:34:41'),
('103.45.246.42',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 12:15:52','2025-06-03 12:15:52','2025-06-03 12:15:52','2025-06-03 12:15:52'),
('91.223.169.235',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 10:37:11','2025-06-03 10:37:11','2025-06-03 10:37:11','2025-06-03 10:37:11'),
('184.105.247.195','scan-14.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 09:20:13','2025-06-03 09:20:13','2025-06-03 09:20:13','2025-06-03 09:20:13'),
('150.95.26.204','v150-95-26-204.a00d.g.bkk1.static.cnode.io','YES',3,0,0,0,0,0,0,0,0,0,4,3,0,0,110,0,0,0,0,0,0,0,'2025-06-03 04:45:32','2025-06-03 04:49:23','2025-06-03 04:45:32','2025-06-03 04:49:24'),
('104.155.40.111',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-03 01:18:53','2025-06-03 01:18:53','2025-06-03 01:18:53','2025-06-03 01:18:53'),
('167.94.145.109',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-03 00:53:44','2025-06-03 00:53:54','2025-06-03 00:53:44','2025-06-03 00:53:56'),
('157.245.114.132',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-03 00:21:29','2025-06-03 00:21:29','2025-06-03 00:21:29','2025-06-03 00:21:29'),
('89.70.112.188',NULL,'YES',1,0,0,0,0,0,2,0,0,0,2,1,0,0,115,0,0,0,0,0,0,0,'2025-06-02 22:04:47','2025-06-02 22:05:30','2025-06-02 22:04:47','2025-06-02 22:05:30'),
('20.65.193.205','azpdss8hh31k.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 18:19:09','2025-06-02 18:19:09','2025-06-02 18:19:09','2025-06-02 18:19:09'),
('20.106.57.141','azpdcsxwfxxy.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 16:51:42','2025-06-02 16:51:42','2025-06-02 16:51:42','2025-06-02 16:51:42'),
('198.235.24.59',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 16:32:23','2025-06-02 16:32:23','2025-06-02 16:32:23','2025-06-02 16:32:34'),
('167.94.138.169',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-02 15:08:42','2025-06-02 15:09:09','2025-06-02 15:08:42','2025-06-02 15:09:10'),
('103.203.57.18',NULL,'YES',1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 13:26:51','2025-06-02 13:26:51','2025-06-02 13:26:51','2025-06-02 13:26:57'),
('48.216.243.151','azpdegpjn8g0.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 10:25:02','2025-06-02 10:25:02','2025-06-02 10:25:02','2025-06-02 10:25:02'),
('143.244.128.47',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 07:00:23','2025-06-02 07:00:23','2025-06-02 07:00:23','2025-06-02 07:00:23'),
('74.82.47.4','scan-11.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 05:11:30','2025-06-02 05:11:30','2025-06-02 05:11:30','2025-06-02 05:11:30'),
('13.89.125.227','azpdcs37khkp.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 04:17:23','2025-06-02 04:17:23','2025-06-02 04:17:23','2025-06-02 04:17:23'),
('3.137.141.123','ec2-3-137-141-123.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 02:36:32','2025-06-02 02:36:32','2025-06-02 02:36:33','2025-06-02 02:36:33'),
('157.230.8.75',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-02 00:17:24','2025-06-02 00:17:24','2025-06-02 00:17:24','2025-06-02 00:17:24'),
('154.47.30.141',NULL,'YES',0,0,0,0,0,0,1,0,0,0,3,0,0,0,2,0,0,0,0,0,0,0,'2025-06-01 21:56:01','2025-06-01 21:56:08','2025-06-01 21:56:01','2025-06-01 21:56:09'),
('220.250.10.210',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 16:32:48','2025-06-01 16:32:48','2025-06-01 16:32:48','2025-06-01 16:32:48'),
('34.77.182.94',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 14:26:20','2025-06-01 14:26:20','2025-06-01 14:26:20','2025-06-01 14:26:20'),
('223.233.84.117',NULL,'YES',0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'2025-05-30 14:47:17','2025-06-01 13:31:41','2025-05-30 14:47:17','2025-05-30 14:47:17'),
('128.203.203.196','azpdcgcif6ni.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 12:13:23','2025-06-01 12:13:23','2025-06-01 12:13:23','2025-06-01 12:13:23'),
('205.210.31.147',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 07:39:07','2025-06-01 07:39:07','2025-06-01 07:39:07','2025-06-01 07:39:07'),
('162.142.125.43',NULL,'YES',10,0,0,1,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,'2025-06-01 07:05:44','2025-06-01 07:05:55','2025-06-01 07:05:44','2025-06-01 07:05:56'),
('206.168.34.64',NULL,'YES',5,0,0,1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,'2025-06-01 06:35:41','2025-06-01 06:35:52','2025-06-01 06:35:41','2025-06-01 06:35:52'),
('139.162.70.53',NULL,'YES',1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 06:03:01','2025-06-01 06:03:01','2025-06-01 06:03:01','2025-06-01 06:03:01'),
('170.64.134.89',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 03:11:34','2025-06-01 03:11:34','2025-06-01 03:11:34','2025-06-01 03:11:34'),
('216.218.206.68','scan-07.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-06-01 01:25:12','2025-06-01 01:25:12','2025-06-01 01:25:12','2025-06-01 01:25:12'),
('137.184.39.58',NULL,'YES',2,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,'2025-06-01 01:11:53','2025-06-01 01:11:53','2025-06-01 01:11:53','2025-06-01 01:11:53'),
('3.144.245.14','ec2-3-144-245-14.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 23:52:22','2025-05-31 23:52:22','2025-05-31 23:52:22','2025-05-31 23:52:22'),
('64.227.110.161','1698d28f.tidalcoinage.internet-measurement.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 15:55:51','2025-05-31 15:55:51','2025-05-31 15:55:53','2025-05-31 15:55:53'),
('20.163.14.234','azpdwsxs9gxv.stretchoid.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 14:02:59','2025-05-31 14:02:59','2025-05-31 14:02:59','2025-05-31 14:02:59'),
('35.216.129.240',NULL,'NO',0,0,0,0,13,0,0,0,0,0,2,2,0,0,9,0,0,0,0,0,0,0,'2025-05-31 06:29:57','2025-05-31 06:30:01','2025-05-31 06:29:57','2025-05-31 06:30:01'),
('64.62.197.77','scan-46a.shadowserver.org','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 04:49:32','2025-05-31 04:49:32','2025-05-31 04:49:32','2025-05-31 04:49:32'),
('20.169.106.110',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 04:06:56','2025-05-31 04:06:56','2025-05-31 04:06:56','2025-05-31 04:06:56'),
('3.22.234.7','ec2-3-22-234-7.us-east-2.compute.amazonaws.com','YES',1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 03:48:05','2025-05-31 03:48:05','2025-05-31 03:48:06','2025-05-31 03:48:06'),
('34.38.121.245',NULL,'NO',0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-31 00:18:28','2025-05-31 00:18:28','2025-05-31 00:18:28','2025-05-31 00:18:28'),
('185.195.232.134',NULL,'YES',0,0,0,1,0,0,0,0,0,0,3,0,0,0,2,0,0,0,0,0,0,0,'2025-05-31 00:13:29','2025-05-31 00:13:30','2025-05-31 00:13:29','2025-05-31 00:13:30'),
('198.235.24.13',NULL,'YES',1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,'2025-05-30 20:02:08','2025-05-30 20:02:08','2025-05-30 20:02:08','2025-05-30 20:02:08'),
('154.198.73.247',NULL,'YES',2,0,0,2,0,0,0,0,0,0,1,2,0,0,46,0,0,0,0,0,0,0,'2025-05-30 14:47:08','2025-05-30 14:48:25','2025-05-30 14:47:08','2025-05-30 14:48:35');
/*!40000 ALTER TABLE `host_cache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosts` (
  `HOST` char(255) CHARACTER SET ascii COLLATE ascii_general_ci DEFAULT NULL,
  `CURRENT_CONNECTIONS` bigint NOT NULL,
  `TOTAL_CONNECTIONS` bigint NOT NULL,
  `MAX_SESSION_CONTROLLED_MEMORY` bigint unsigned NOT NULL,
  `MAX_SESSION_TOTAL_MEMORY` bigint unsigned NOT NULL,
  UNIQUE KEY `HOST` (`HOST`)
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hosts`
--

LOCK TABLES `hosts` WRITE;
/*!40000 ALTER TABLE `hosts` DISABLE KEYS */;
/*!40000 ALTER TABLE `hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `innodb_redo_log_files`
--

DROP TABLE IF EXISTS `innodb_redo_log_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `innodb_redo_log_files` (
  `FILE_ID` bigint NOT NULL COMMENT 'Id of the file.',
  `FILE_NAME` varchar(2000) NOT NULL COMMENT 'Path to the file.',
  `START_LSN` bigint NOT NULL COMMENT 'LSN of the first block in the file.',
  `END_LSN` bigint NOT NULL COMMENT 'LSN after the last block in the file.',
  `SIZE_IN_BYTES` bigint NOT NULL COMMENT 'Size of the file (in bytes).',
  `IS_FULL` tinyint NOT NULL COMMENT '1 iff file has no free space inside.',
  `CONSUMER_LEVEL` int NOT NULL COMMENT 'All redo log consumers registered on smaller levels than this value, have already consumed this file.'
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `innodb_redo_log_files`
--

LOCK TABLES `innodb_redo_log_files` WRITE;
/*!40000 ALTER TABLE `innodb_redo_log_files` DISABLE KEYS */;
INSERT INTO `innodb_redo_log_files` VALUES
(4,'/rdsdbdata/log/innodb/#innodb_redo/#ib_redo4',33554432,100661248,67108864,0,0);
/*!40000 ALTER TABLE `innodb_redo_log_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keyring_component_status`
--

DROP TABLE IF EXISTS `keyring_component_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyring_component_status` (
  `STATUS_KEY` varchar(256) NOT NULL,
  `STATUS_VALUE` varchar(1024) NOT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyring_component_status`
--

LOCK TABLES `keyring_component_status` WRITE;
/*!40000 ALTER TABLE `keyring_component_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `keyring_component_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keyring_keys`
--

DROP TABLE IF EXISTS `keyring_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyring_keys` (
  `KEY_ID` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `KEY_OWNER` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `BACKEND_KEY_ID` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyring_keys`
--

LOCK TABLES `keyring_keys` WRITE;
/*!40000 ALTER TABLE `keyring_keys` DISABLE KEYS */;
/*!40000 ALTER TABLE `keyring_keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_status`
--

DROP TABLE IF EXISTS `log_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_status` (
  `SERVER_UUID` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `LOCAL` json NOT NULL,
  `REPLICATION` json NOT NULL,
  `STORAGE_ENGINES` json NOT NULL
) ENGINE=PERFORMANCE_SCHEMA DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_status`
--

LOCK TABLES `log_status` WRITE;
/*!40000 ALTER TABLE `log_status` DISABLE KEYS */;
