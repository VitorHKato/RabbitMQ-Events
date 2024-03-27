import pika
import sys

# Estabelece uma conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Criado uma exchange do tipo 'topic_logs' do tipo topic (a mensagem vai para quem tiver um binding key de interesse)
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Cria uma fila vazia de nome aleatório, deleta a fila quando a conexão fechar
result = channel.queue_declare(queue='', exclusive=True)

queue_name = result.method.queue

# Lê do terminal a string passada
binding_keys = sys.argv[1:]

# Se não for passada nenhuma string, alerta e fecha o programa
if not binding_keys:
    sys.stderr.write('Usage: %s [binding_key]... \n' % sys.argv[0])
    sys.exit(0)

# Faz a conexão da fila com a binding key passada
for b in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=b)

print(' [*} Waiting for logs. Press CTRL+C to cancel')

# Sobrescrevendo a função de retorno da mensagem da fila
def callback(ch, method, properties, body):
    print(f" [X] {method.routing_key}:{body}")

# Informa a fila que ela receberá mensagens da função callback
# Informa que ela só enviará um pedido para um receptor se receber o ack dele
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()