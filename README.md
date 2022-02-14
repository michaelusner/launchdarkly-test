# Configuration
To create the react app, the following steps were necessary:
  ```
  docker run -it --rm -v $(pwd):/app node:latest bash
  (in container)
  apt update && apt upgrade -y
  yarn global add create-react-app
  yarn create react-app front-end
  cd front-end
  chown node:node -R .
  yarn install
  ```
