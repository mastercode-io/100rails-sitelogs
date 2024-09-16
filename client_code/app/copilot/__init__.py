import anvil.server
import time

copilot_keys = anvil.server.call('get_secrets', 'openai_api_key', 'copilot_assistant_id')
OPENAI_API_KEY = copilot_keys.get('openai_api_key')
COPILOT_ASSISTANT_ID = copilot_keys.get('copilot_assistant_id')


class Copilot:

    def __init__(self, api_key=None, assistant_id=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.assistant_id = assistant_id or COPILOT_ASSISTANT_ID
        self.thread_id = anvil.server.call('openai_init_client', api_key=self.api_key)
        self.current_run_id = None

    def send_message(self, question):
        response = anvil.server.call(
            'openai_send_message',
            question,
            assistant_id=self.assistant_id,
            thread_id=self.thread_id,
        )
        print('send_message', response)
        return response

    def retrieve_response(self):
        response = anvil.server.call(
            'openai_retrieve_response',
            thread_id=self.thread_id,
            run_id=self.current_run_id,
        )
        return response

    def get_response(self, question):
        response = self.send_message(question)
        self.current_run_id = response['id']
        while response['status'] == 'queued' or response['status'] == 'in_progress':
            time.sleep(0.5)
            response = self.retrieve_response()
            # print('get_response', response)
        response = anvil.server.call(
            'openai_get_messages',
            thread_id=self.thread_id,
        )
        return response
