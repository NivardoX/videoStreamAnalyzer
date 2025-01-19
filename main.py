
import argparse
from threading import Thread
from producer.Producer import Producer, MockedProducer

def produce(camera):
    """
    This function uses the standard Producer.
    """
    producer = Producer(camera['id'], camera['url'])
    producer.start()

def produce_mocked(camera, test_id,use_celery=True, total_images=3000,fps=10):
    """
    This function uses the MockedProducer.
    """
    producer = MockedProducer(
        camera['id'],
        camera['url'],
        use_celery=use_celery,
        total_images=total_images,
        test_id=test_id,
        fps=fps,
    )
    producer.start()

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Script to launch producers for cameras.")

    # Example arguments:
    parser.add_argument('--cameras', type=int, default=3,
                        help="How cameras will be used to produce.")
    parser.add_argument('--use-celery', action='store_true',
                        help="If using the mocked producer, enable Celery for tasks.")
    parser.add_argument('--total-images', type=int, default=200,
                        help="How many frames to produce for each camera (mocked producer only).")
    parser.add_argument('--test', type=str,
                        help="Id of the test")

    # Parse command line arguments
    args = parser.parse_args()

    # Loop over cameras, start a thread for each
    for camera in range(args.cameras):
        camera_info = {"id": f"Mock{camera}", "url": None}
        thread = Thread(
            target=produce_mocked,
            args=(camera_info,args.test,args.use_celery, args.total_images)
        )

        # Start the producer thread
        thread.start()
