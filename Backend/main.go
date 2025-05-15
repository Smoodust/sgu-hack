package main

import (
	"SGUHACATON2025/handlers"
	handlers2 "SGUHACATON2025/handlers/db"
	"SGUHACATON2025/middleware"
	"SGUHACATON2025/pkg/client/postgreSQL"
	"context"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"time"
)

func main() {
	router := gin.Default()
	postgreSQLClient, err := postgreSQL.NewClient(context.TODO(), 3, postgreSQL.StorageConfig{
		"localhost",
		"5432",
		"postgres",
		"admin",
		"admin",
	})
	if err != nil {
		log.Fatalf("%v", err)
	}
	handlRepositiry := handlers2.NewRepository(postgreSQLClient)

	router.Use(middleware.LoggerMiddleware()) // Подключаем Middleware
	router.Use(cors.New(cors.Config{
		AllowOrigins: []string{
			"http://localhost",
			"http://localhost:80",
			"http://frontend",    // Для Docker-сети
			"http://frontend:80", // Для Docker-сети с портом
		},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Length", "Content-Type", "Authorization", "X-Requested-With"},
		ExposeHeaders:    []string{"Content-Length", "X-Total-Count"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	handler := handlers.NewHandler(handlRepositiry) // Подключаем Handlers
	handler.Register(router)                        // Регистрация хэндлера

	// Запускаем роутер
	start(router)
}

func start(router *gin.Engine) {
	server := &http.Server{
		Addr:         ":8080",
		Handler:      router,
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}
	log.Fatalln(server.ListenAndServe())
}
