   # YouTube Transcribe

   This application transcribes YouTube videos using the Vosk speech recognition model.

   ## Prerequisites

   - Docker

   ## Installation

   1. Clone the repository:
      ```
      git clone https://github.com/your-username/youtube-transcribe.git
      cd youtube-transcribe
      ```

   2. Build the Docker image:
      ```
      docker build -t youtube-transcribe .
      ```

   3. Run the Docker container:
      ```
      docker run -d --name youtube-transcribe -p 5001:5000 youtube-transcribe
      ```

   ## Usage

   Access the application at `http://localhost:5001/transcribe?url=YOUR_YOUTUBE_URL`

   Replace `YOUR_YOUTUBE_URL` with the URL of the YouTube video you want to transcribe.

   ## License

   [MIT License](LICENSE)