package handlers

import (
	handlers "SGUHACATON2025/handlers"
	postgreSQL "SGUHACATON2025/pkg/client/postgreSQL"
	"context"
	"errors"
	"fmt"
	"log"
	"strings"

	"github.com/jackc/pgconn"
)

type repository struct {
	client postgreSQL.Client
}

func NewRepository(client postgreSQL.Client) handlers.Repository {
	return &repository{
		client: client,
	}
}

func formatQuery(q string) string {
	return strings.ReplaceAll(strings.ReplaceAll(q, "\t", ""), "\n", " ")
}

func (r *repository) Create(ctx context.Context, user *handlers.User) error {
	q := `INSERT INTO user 
		    (name,password) 
		VALUES 
		       ($1, $2) 
		RETURNING id
	`
	log.Print(fmt.Sprintf("SQL Query: %s", formatQuery(q)))
	if err := r.client.QueryRow(ctx, q, user.Name, user.Password).Scan(&user.ID); err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) {
			pgErr = err.(*pgconn.PgError)
			newErr := fmt.Errorf(fmt.Sprintf("SQL Error: %s, Detail: %s, Where: %s, Code: %s, SQLState: %s", pgErr.Message, pgErr.Detail, pgErr.Where, pgErr.Code, pgErr.SQLState()))
			log.Print(newErr)
			return newErr
		}
		return err
	}

	return nil
}

func (r *repository) FindAll(ctx context.Context) (u []handlers.User, err error) {
	q := `
		SELECT id, name, password FROM user;
	`
	log.Print(fmt.Sprintf("SQL Query: %s", formatQuery(q)))

	rows, err := r.client.Query(ctx, q)
	if err != nil {
		return nil, err
	}

	users := make([]handlers.User, 0)

	for rows.Next() {
		var usr handlers.User

		err = rows.Scan(&usr.ID, &usr.Name, &usr.Password)
		if err != nil {
			return nil, err
		}

		users = append(users, usr)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return users, nil
}

func (r *repository) FindOne(ctx context.Context, id string) (handlers.User, error) {
	q := `
		SELECT id, name, password FROM user WHERE id = $1
	`
	log.Print(fmt.Sprintf("SQL Query: %s", formatQuery(q)))

	var usr handlers.User
	err := r.client.QueryRow(ctx, q, id).Scan(&usr.ID, &usr.Name, &usr.Password)
	if err != nil {
		return handlers.User{}, err
	}

	return usr, nil
}

func (r *repository) Update(ctx context.Context, user handlers.User) error {
	//TODO implement me
	panic("implement me")
}

func (r *repository) Delete(ctx context.Context, id string) error {
	q := `
			DELETE FROM "user" where id = $1
		`
	log.Print(fmt.Sprintf("SQL Query: %s", formatQuery(q)))

	var usr handlers.User
	err := r.client.QueryRow(ctx, q, id).Scan(&usr.ID)
	if err != nil {
		log.Printf("Error delete user: %s", err)
		return err
	}

	return nil
}

func (r *repository) Check(ctx context.Context, user *handlers.User) error {
	q := `SELECT password FROM user where name = $1`
	log.Print(fmt.Sprintf("SQL Query: %s", formatQuery(q)))

	if err := r.client.QueryRow(ctx, q, user.Name).Scan(&user.Password); err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) {
			pgErr = err.(*pgconn.PgError)
			newErr := fmt.Errorf(fmt.Sprintf("SQL Error: %s, Detail: %s, Where: %s, Code: %s, SQLState: %s", pgErr.Message, pgErr.Detail, pgErr.Where, pgErr.Code, pgErr.SQLState()))
			log.Print(newErr)
			return newErr
		}
		return err
	}

	return nil
}
