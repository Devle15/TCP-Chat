
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;

namespace NetFraming
{
    public static class Frame
    {
        public static void SendString(NetworkStream stream, string text)
        {
            var payload = Encoding.UTF8.GetBytes(text);
            var len = BitConverter.GetBytes(payload.Length);
            if (BitConverter.IsLittleEndian) Array.Reverse(len);
            stream.Write(len, 0, len.Length);
            stream.Write(payload, 0, payload.Length);
        }

        public static string? ReceiveString(NetworkStream stream)
        {
            var lenBuf = ReadExact(stream, 4);
            if (lenBuf == null) return null;
            if (BitConverter.IsLittleEndian) Array.Reverse(lenBuf);
            int len = BitConverter.ToInt32(lenBuf, 0);
            var payload = ReadExact(stream, len);
            if (payload == null) return null;
            return Encoding.UTF8.GetString(payload);
        }

        private static byte[]? ReadExact(NetworkStream stream, int size)
        {
            byte[] buf = new byte[size];
            int read = 0;
            while (read < size)
            {
                int n = stream.Read(buf, read, size - read);
                if (n == 0) return null;
                read += n;
            }
            return buf;
        }
    }
}
