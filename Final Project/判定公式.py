#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:08:01 2023

@author: daixiang
"""
for t in range(1,401):
    
    if (t % 20 != 0 and t % 20 < 17 and t % 20 > 4 
        and (panels[t] == panels[t+1] == panels[t+2] == panels[t+3] == panels[t+4] == sign) 
         or (panels[t] == panels[t+20] == panels[t+40] == panels[t+60] == panels[t+80] == sign)
         or (panels[t] == panels[t+21] == panels[t+42] == panels[t+63] == panels[t+84] == sign)
         or (panels[t] == panels[t+19] == panels[t+38] == panels[t+57] == panels[t+76] == sign)):
        if self.gameinfo[groupnum][3] == 'O':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 2"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
        elif self.gameinfo[groupnum][3] == 'X':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 1"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
            
    elif ((t % 20 == 0 or t % 20 > 16) and (t < 316) 
          and ((panels[t] == panels[t+20] == panels[t+40] == panels[t+60] == panels[t+80] == sign) 
            or (panels[t] == panels[t+19] == panels[t+38] == panels[t+57] == panels[t+76] == sign))):
        if self.gameinfo[groupnum][3] == 'O':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 2"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
        elif self.gameinfo[groupnum][3] == 'X':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 1"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
            
    elif ((t > 316) and (t % 20 < 17) 
          and (panels[t] == panels[t+1] == panels[t+2] == panels[t+3] == panels[t+4] == sign)):
        if self.gameinfo[groupnum][3] == 'O':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 2"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
        elif self.gameinfo[groupnum][3] == 'X':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 1"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
            
    elif ((t < 316) and (t % 20 <= 4) 
          and (panels[t] == panels[t+1] == panels[t+2] == panels[t+3] == panels[t+4] == sign)
          or (panels[t] == panels[t+20] == panels[t+40] == panels[t+60] == panels[t+80] == sign)
          or (panels[t] == panels[t+21] == panels[t+42] == panels[t+63] == panels[t+84] == sign)):
        if self.gameinfo[groupnum][3] == 'O':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 2"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
        elif self.gameinfo[groupnum][3] == 'X':
            for g in The_guys:
                to_sock = self.logged_name2sock[g]
                mysend(to_sock, json.dumps(
                    {"action": "gaming", 'status': 'finish', 'result': "Player 1"}))
            self.gameinfo[groupnum][0] = [i for i in range(1,401)]
            self.gameinfo[groupnum][1] = 0
            self.gameinfo[groupnum][2] = ["0"] * 400
            self.gameinfo[groupnum][3] = ''
        
    