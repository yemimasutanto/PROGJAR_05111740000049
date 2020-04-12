import sys
import os
import json
import uuid
import logging
from queue import Queue


class Chat:
	def __init__(self):
		self.sessions = {}
		self.users = {}
		#kalo mau daftarin user, disini
		self.users['messi'] = {'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['henderson'] = {'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker'] = {'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['alice'] = {'nama': 'Alice Smith', 'negara': 'Wales', 'password': 'passwd', 'incoming': {}, 'outgoing': {}}

	def proses(self, data):
		j = data.split(" ")
		try:
			#daftar command yang bisa digunakan dalam aplikasi ini
			command = j[0].strip()
			#login
			if (command == 'auth'):
				username = j[1].strip()
				password = j[2].strip()
				logging.warning("AUTH: auth {} {}".format(username, password))
				return self.autentikasi_user(username, password)
			#berkirim pesan
			elif (command == 'send'):
				sessionid = j[1].strip()
				usernameto = j[2].strip()
				message = ""
				for w in j[3:]:
					message = "{} {}".format(message, w)
				usernamefrom = self.sessions[sessionid]['username']
				logging.warning(
					"SEND: session {} send message from {} to {}".format(sessionid, usernamefrom, usernameto))
				return self.send_message(sessionid, usernamefrom, usernameto, message)
			#cek pesan masuk dari luar
			elif (command == 'inbox'):
				sessionid = j[1].strip()
				username = self.sessions[sessionid]['username']
				logging.warning("INBOX: {}".format(sessionid))
				return self.get_inbox(username)
			#cek user yang sedang online
			elif (command == 'status'):
				sessionid = j[1].strip()
				logging.warning("ACTIVE USER: {}".format(sessionid))
				return self.status()
			#logout/mengakhiri sesi
			elif (command == 'logout'):
				sessionid = j[1].strip()
				logging.warning("LOGOUT: {}".format(sessionid))
				return self.logout(sessionid)

			else:
				return {'status': 'ERROR', 'message': 'Sorry, wrong protocol'}
		except KeyError:
			return {'status': 'ERROR', 'message': 'Information not found [Key Error]'}
		except IndexError:
			return {'status': 'ERROR', 'message': 'Sorry, wrong protocol [Index Error]'}

	#fungsi authentikasi/login user
	def autentikasi_user(self, username, password):
		if (username not in self.users):
			return {'status': 'ERROR', 'message': 'Sorry, user not found. Check again.'}
		if (self.users[username]['password'] != password):
			return {'status': 'ERROR', 'message': 'Sorry, wrong password. Check again.'}
		tokenid = str(uuid.uuid4())
		self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}
		return {'status': 'OK', 'tokenid': tokenid}

	def get_user(self, username):
		if (username not in self.users):
			return False
		return self.users[username]

	#fungsi kirim pesan
	def send_message(self, sessionid, username_from, username_dest, message):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session not found'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)

		if (s_fr == False or s_to == False):
			return {'status': 'ERROR', 'message': 'Sorry, user not found. Check again.'}

		message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
		outqueue_sender = s_fr['outgoing']
		inqueue_receiver = s_to['incoming']
		try:
			outqueue_sender[username_from].put(message)
		except KeyError:
			outqueue_sender[username_from] = Queue()
			outqueue_sender[username_from].put(message)
		try:
			inqueue_receiver[username_from].put(message)
		except KeyError:
			inqueue_receiver[username_from] = Queue()
			inqueue_receiver[username_from].put(message)
		return {'status': 'OK', 'message': 'Message Sent'}

	def get_inbox(self, username):
		s_fr = self.get_user(username)
		incoming = s_fr['incoming']
		msgs = {}
		for users in incoming:
			msgs[users] = []
			while not incoming[users].empty():
				msgs[users].append(s_fr['incoming'][users].get_nowait())

		return {'status': 'OK', 'messages': msgs}

	#fungsi logout
	def logout(self, sessionid):
		del self.sessions[sessionid]
		return {'status': 'OK', 'messages': "Session Closed"}

	#fungsi untuk cek yang online
	def status(self):
		token = list(self.sessions.keys())
		status = ""
		for i in token:
			status = status + self.sessions[i]['username'] + ", "
		return {'status': 'OK', 'message': '{}'.format(status)}