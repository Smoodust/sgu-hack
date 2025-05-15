package handlers

import (
	"SGUHACATON2025/pkg/utils/jwt"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
)

const (
	loginURL    = "/login/"
	registerURL = "/registration/"
)

type handler struct {
	db Repository
}

// NewHandler создает новый обработчик с подключением к базе данных
func NewHandler(DB Repository) Handler {
	return &handler{
		db: DB,
	}
}

// Register регистрирует все маршруты для авторизации, пользователей и чатов.
func (h *handler) Register(router *gin.Engine) {
	// Публичные маршруты (без JWT)
	public := router.Group("/")
	{
		// Регистрация и Login
		public.POST(registerURL, h.registration)
		public.POST(loginURL, h.login)

	}

	//// Защищённые маршруты (с JWT)
	//private := router.Group("/")
	//private.Use(middleware.AuthMiddleware()) // Проверка JWT
	//{
	//	private.GET("/user", h.getUser)
	//}

}

func (h *handler) registration(c *gin.Context) {
	var user User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.db.Create(c.Request.Context(), &user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	log.Printf("[REGISTRATION] Пользователь успешно зарегистрирован: %s", user.Name)
	c.JSON(http.StatusOK, gin.H{"message": "Пользователь успешно зарегистрирован"})
}

func (h *handler) login(c *gin.Context) {
	var userInput User
	if err := c.ShouldBindJSON(&userInput); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user User
	if err := h.db.Check(c.Request.Context(), &user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if !jwt.CheckPasswordHash(userInput.Password, user.Password) {
		log.Printf("[LOGIN] Неверный пароль для пользователя: %s", userInput.Name)
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Неверный логин или пароль"})
		return
	}

	token, err := jwt.GenerateJWT(user.Name)
	if err != nil {
		log.Printf("[LOGIN] Ошибка генерации токена для пользователя %s: %v", userInput.Name, err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Ошибка при создании токена"})
		return
	}

	log.Printf("[LOGIN] Токен успешно сгенерирован для пользователя: %s", userInput.Name)
	c.JSON(http.StatusOK, gin.H{"token": token})
}
