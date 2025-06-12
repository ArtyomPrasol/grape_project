import threading
from queue import Queue
import os
from database import Database
from models import ModelManager
from minio_storage import upload_file, create_minio_client
from config import REQ_FOLDER

class QueueProcessor:
    def __init__(self):
        self.request_queue = Queue()
        self.db = Database()
        self.model_manager = ModelManager()
        self.minio_client = create_minio_client()
        self.worker_thread = None

    def start(self):
        """Запускает обработчик очереди в отдельном потоке"""
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def add_task(self, task_id, filename):
        """Добавляет задачу в очередь"""
        self.request_queue.put((task_id, filename))

    def _process_queue(self):
        """Обрабатывает задачи из очереди"""
        while True:
            try:
                task = self.request_queue.get()
                if task is None:
                    break

                task_id, filename = task
                image_path = os.path.join(REQ_FOLDER, filename)

                best_img, class_id = self.model_manager.process_image(
                    image_path,
                    self.db.bind_class_model
                )

                if class_id == -1:
                    self.db.update_request_status(task_id, -1, filename)
                else:
                    new_filename = 'r' + filename
                    if upload_file(self.minio_client, best_img[0], new_filename):
                        self.db.update_request_status(task_id, class_id, new_filename)
                        os.remove(image_path)
                        self.model_manager.clear_cropped_images()

            except Exception as e:
                print(f"Error processing queue: {str(e)}")
            finally:
                self.request_queue.task_done()

    def stop(self):
        """Останавливает обработчик очереди"""
        self.request_queue.put(None)
        if self.worker_thread:
            self.worker_thread.join()
        self.db.close() 