FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o redirect-service ./services/redirect-service/main.go


FROM alpine:latest

RUN apk upgrade --no-cache && apk add --no-cache ca-certificates

WORKDIR /root/

COPY --from=builder /app/redirect-service .

EXPOSE 8002

CMD ["./redirect-service"]
