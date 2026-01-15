# ⚡ LAN Share

A lightweight, modern file sharing server for local networks. Built with Python's standard library, no external dependencies required.

## Features

- 🚀 **Zero Dependencies** - Uses only Python standard library
- 📱 **Responsive Design** - Beautiful UI that works on desktop and mobile
- 📤 **File Upload** - Drag-and-drop style file uploads with progress tracking
- 📂 **Directory Browsing** - Navigate directories with breadcrumb-style back button
- 🔄 **Streaming Upload** - Efficient memory usage with streaming POST to disk
- 🎨 **Modern Interface** - Clean, professional design with smooth interactions

## Quick Start

### Prerequisites

- Python 3.6+
- Any device on the same local network

### Installation

```bash
git clone https://github.com/ulolol/LANShare.git
```

### Usage

Run the server from the directory you want to share:

```bash
python3 Simple_File_Server.py
```

The server will start and display:

```
🚀 LAN Share Server Live!
🔗 URL: http://192.168.x.x:42069
📂 Folder: /current/directory
```

Open the URL in any browser on your local network to access the file sharing interface.

## Configuration

Edit the `PORT` variable in `Simple_File_Server.py` to change the listening port:

```python
PORT = 42069  # Change this to your preferred port
```

## Features Explained

### File Browsing
- View all files and folders in the current directory
- Click on folders to navigate
- See file size and last modified date
- Use "Go Back" button to navigate up directory levels

### File Uploading
- Select a file from your device using the upload input
- Click "Push to Server ⚡" to upload
- Real-time progress bar shows upload percentage and speed
- Automatic page refresh on successful upload

### Download
- Click any file to download it
- Downloads handled efficiently by standard HTTP

## How It Works

- **GET Requests** - Serve files and generate directory listings
- **POST Requests** - Handle file uploads with multipart/form-data
- **Streaming** - Large file uploads processed in memory-efficient chunks
- **Threading** - `ThreadingHTTPServer` handles multiple concurrent connections

## Security Considerations

⚠️ **Important**: This server is designed for trusted local networks only.

- No authentication or access control
- Runs on your local network (not exposed to internet by default)
- Use only on private, trusted networks
- Do not expose to untrusted networks or the internet

## Customization

The server uses self-contained CSS for styling. To customize the appearance, edit the `<style>` section in the `list_directory` method.

### Color Scheme

Default colors are defined as CSS variables:

```css
:root {
    --primary: #4f46e5;  /* Primary color (indigo) */
    --bg: #f8fafc;       /* Background */
    --card: #ffffff;     /* Card background */
    --text: #1e293b;     /* Text color */
}
```

## Troubleshooting

**Can't access the server from other devices?**
- Ensure you're on the same network
- Check your firewall settings
- Verify the IP address is correct (shown on startup)

**Port already in use?**
- Change the `PORT` variable to a different number
- Check what's using the port: `lsof -i :42069` (macOS/Linux)

**Upload not working?**
- Ensure you have write permissions in the directory
- Check available disk space
- Try uploading a smaller file first

## Requirements

- Python 3.6 or higher
- Standard library modules only: `http.server`, `socketserver`, `os`, `socket`, `re`, `html`, `datetime`

## License

MIT License - Feel free to use and modify for your needs.

## Contributing

Found a bug or have an improvement? Feel free to submit issues and pull requests!

---

**Made with ❤️ by Vidish for seamless local network file sharing**
