# RabbitMQ-Events
Event-Oriented architecture using RabbitMQ and Python

To test with 2 consumers. Run the following in 2 different terminals.

  python consumer.py "message.#"
  python consumer.py "logs.*" "*.errors" 

And the following to send the messages.

  python publisher.py "logs.asdasd" "Log Message"
  python publisher.py "message.asddas.asddas" "Error Message"
