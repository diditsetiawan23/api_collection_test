import asyncio
from function.wrap import PostmanNewman

# Initialize Wrapper
test = PostmanNewman

# Calling all test
test.execute_postman_test()
# Sending report
test.send_result_to_email()
asyncio.run(test.send_result_to_telegram())