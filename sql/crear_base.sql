-- Ejecutar en phpMyAdmin antes de migrate. Django crea las tablas.
CREATE DATABASE IF NOT EXISTS hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hotel_db;
SELECT VERSION();
