import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
import tester_node


class OrderSubscriber(Node):

	def __init__(self):
		super().__init__('Order_subscriber')
		self.start_flag = False
		qos_profile = QoSProfile(depth=10)
		self.order_subscriber = self.create_subscription(
			String,
			'OrderDY',
			self.subscribe_order_callback,
			qos_profile
		)

	def subscribe_order_callback(self, msg):
		self.get_logger().info('Received DY message {}'.format(msg.data))
		if msg.data == "Start":
			self.start_flag = True

def main(args=None):
	rclpy.init(args=args)
	node = OrderSubscriber()
	try:

		while True:
			rclpy.spin_once(node)
			if node.start_flag:
				break
		# pass
	except KeyboardInterrupt:
		node.get_logger().info('Keyboard Interrrupt')
	finally:
		node.destroy_node()
		rclpy.shutdown()


if __name__=='__main__':
	main()
	tester_node.main()
