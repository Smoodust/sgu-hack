package handlers

type User struct {
	ID           string `json:"-"`
	Name         string `json:"name"`
	Password string `json:"password"`
}
