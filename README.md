# workshop_mcp_litellm
这个workshop基于[crewai(litellm)+mcp.run](https://docs.mcp.run/integrating/tutorials/mcpx-crewai-python)，通过调用AWS bedrock nova，实现multi-agent旅游咨询顾问demo，同时增加了日志配置，以便于讲解。


### AWS Bedrock 介绍
AWS Bedrock 是一种基础设施服务，提供了一系列的基础设施和服务，使开发者能够更快速地构建和部署应用程序。在本项目中，AWS Bedrock 用于提供底层模型服务，为 agent 提供所需的计算资源和模型支持。