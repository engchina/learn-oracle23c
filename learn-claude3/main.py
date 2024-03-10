from dotenv import load_dotenv, find_dotenv
import anthropic

# read local .env file
# find_dotenv 函数通常用于搜索和定位目录树中的 .env 文件，而 load_dotenv 函数用于将 .env 文件中的变量加载到环境中。
_ = load_dotenv(find_dotenv())

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)


def chat(content):
    return client.messages.create(
        # model="claude-3-opus-20240229",
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": content}
        ]
    )


response = chat("一个矩形的长是10厘米，宽是5厘米，求它的面积。")
print(response.content[0].text)
