/*
  Warnings:

  - You are about to drop the `Price` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Price";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "Aerodar" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "departure" TEXT NOT NULL,
    "appointment" TEXT NOT NULL,
    "AK" TEXT NOT NULL,
    "cost" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Aerosib" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "departure" TEXT NOT NULL,
    "appointment" TEXT NOT NULL,
    "AK" TEXT NOT NULL,
    "cost" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Artis" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "departure" TEXT NOT NULL,
    "appointment" TEXT NOT NULL,
    "AK" TEXT NOT NULL,
    "cost" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Mdcargo" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "departure" TEXT NOT NULL,
    "appointment" TEXT NOT NULL,
    "AK" TEXT NOT NULL,
    "cost" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Transcomavia" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "departure" TEXT NOT NULL,
    "appointment" TEXT NOT NULL,
    "AK" TEXT NOT NULL,
    "cost" TEXT NOT NULL
);
