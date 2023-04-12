package main

import (
	"fmt"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DSN = fmt.Sprintf(`
	host=%s 
	user=%s 
	password=%s  
	dbname=%s
	port=5432 
	sslmode=disable 
	TimeZone=Asia/Makassar`,
	"apps.postgres",
	"admin",
	"admin",
	"music",
)

func Migrate() {
	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  DSN,
		PreferSimpleProtocol: true,
	}), &gorm.Config{})
	if err != nil {
		log.Fatal(err.Error())
	}
	if err = db.AutoMigrate(&Music{}); err != nil {
		log.Fatal(err.Error())
	}
}

func Database() *gorm.DB {
	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  DSN,
		PreferSimpleProtocol: true,
	}), &gorm.Config{})
	if err != nil {
		log.Fatal(err.Error())
	}
	return db
}
