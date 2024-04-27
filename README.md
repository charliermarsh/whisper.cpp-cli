# whisper.cpp-py

A Python wrapper around the [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp) CLI.

Packages [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp) into pre-built, `pip`-installable
wheels, for macOS and Linux.

## Installation

Available on PyPI, with pre-built wheels for macOS and Linux:

```bash
pip install whisper.cpp-py
```

Once installed, `whisper-cpp` will be exposed as a command-line tool:

```bash
whisper-cpp --help
```

## Usage

Following Simon Willison's [_Transcribing MP3s with whisper-cpp on macOS_](https://til.simonwillison.net/macos/whisper-cpp),
once installed, you can download a Whisper model file:

```bash
curl -o ggml-large-v3-q5_0.bin -L 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-q5_0.bin?download=true'
```

Convert from MP3 to 16kHz WAV, if necessary:

```bash
ffmpeg -i input.mp3 -ar 16000 input.wav
```

And transcribe audio, as follows:

```bash
whisper-cpp -m ggml-large-v3-q5_0.bin input.wav --output-txt
```

## Development

[`whisper.cpp`](https://github.com/ggerganov/whisper.cpp) is compiled without any CPU or GPU
acceleration.

In the future, I'd like to distribute builds with
[Core ML support](https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#core-ml-support),
[CUDA support](https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#nvidia-gpu-support), and
more, given `whisper.cpp`'s own support for these features.

The latest release compiles against [`v1.5.5`](https://github.com/ggerganov/whisper.cpp/releases/tag/v1.5.5).

## License

MIT
