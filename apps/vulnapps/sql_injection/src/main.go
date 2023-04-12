package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func index(c *gin.Context) {
	c.File("index.html")
}

func search(c *gin.Context) {
	var music Music
	search := c.PostForm("search")
	if search == "" {
		c.JSON(http.StatusNotFound, gin.H{
			"message": "not found",
		})
		return
	}
	log.Println(c.GetHeader("User-Agent"))
	result, err := music.Search(search)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusAccepted, result)
}

func initdb() {
	file, err := os.OpenFile("/var/log/app/app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}
	log.SetOutput(file)
	db := Database()
	db.Migrator().DropTable(&Music{})
	Migrate()
	musics := []Music{
		{Title: "Faded", Author: "Alan Walker"},
		{Title: "Strange Fruit", Author: "Billie Holiday"},
		{Title: "Heartbreak Hotel", Author: "Elvis Presley"},
	}
	for _, a := range musics {
		a.Add()
	}
}

func main() {

	initdb()
	r := gin.Default()
	r.GET("/", index)
	r.POST("/", search)
	r.Run("0.0.0.0:8000")

}
