#!/usr/bin/expect -f

spawn bluetoothctl
send "power on\r"
send "agent on\r"
send "default-agent\r"
send "scan on\r"
send "pair 41:42:70:A4:04:33\r"
send "trust 41:42:70:A4:04:33\r"
send "connect 41:42:70:A4:04:33\r"
send "quit\r"
expect eof
