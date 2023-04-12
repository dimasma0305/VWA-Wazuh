package main

import (
	"gorm.io/gorm"
)

type Music struct {
	gorm.Model
	Title        string `gorm:"not null;unique"`
	TitleTokens  string `gorm:"type:tsvector"`
	Author       string `gorm:"not null"`
	AuthorTokens string `gorm:"type:tsvector"`
}

func (music *Music) Add() error {
	db := Database()
	new_music := &Music{
		Title:        music.Title,
		TitleTokens:  music.Title,
		Author:       music.Author,
		AuthorTokens: music.Author,
	}
	if err := db.Create(new_music).Error; err != nil {
		return err
	}
	return nil
}

func (music *Music) Search(search_string string) (Music, error) {
	db := Database()
	var new_music Music
	rows, err := db.Raw("SELECT title, author FROM musics WHERE title @@ plainto_tsquery('" + search_string + "')").Rows()
	if err != nil {
		return new_music, err
	}
	for rows.Next() {
		db.ScanRows(rows, &new_music)
	}
	return new_music, nil
}
