FROM golang:1.23.8 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /app/main .

FROM build-stage AS test-stage
RUN go test -v ./...

FROM golang:alpine AS production-stage

RUN apk --no-cache add ca-certificates

WORKDIR /app
COPY --from=build-stage /app/main .

RUN chmod +x main

USER nobody:nogroup

ENTRYPOINT ["/app/main"]