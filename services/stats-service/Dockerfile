FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o stats-service ./services/stats-service/main.go


FROM alpine:latest

RUN apk upgrade --no-cache && apk add --no-cache ca-certificates

WORKDIR /root/

COPY --from=builder /app/stats-service .

EXPOSE 8003

CMD ["./stats-service"]
