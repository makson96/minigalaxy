import subprocess
from unittest import TestCase, mock
from unittest.mock import MagicMock

from minigalaxy import launcher
from minigalaxy.game import Game


class Test(TestCase):
    def test1_determine_launcher_type(self):
        files = ['thumbnail.jpg', 'docs', 'support', 'game', 'start.sh', 'minigalaxy-dlc.json', 'gameinfo']
        exp = "start_script"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    @mock.patch('shutil.which')
    def test2_determine_launcher_type(self, mock_shutil_which):
        mock_shutil_which.return_value = True
        files = ['thumbnail.jpg', 'data', 'docs', 'support', 'beneath.ini', 'scummvm', 'start.sh', 'gameinfo']
        exp = "scummvm"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    def test3_determine_launcher_type(self):
        files = ['thumbnail.jpg', 'docs', 'support', 'unins000.exe', 'minigalaxy-dlc.json', 'gameinfo']
        exp = "windows"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    @mock.patch('shutil.which')
    def test4_determine_launcher_type(self, mock_shutil_which):
        mock_shutil_which.return_value = True
        files = ['thumbnail.jpg', 'docs', 'support', 'dosbox', 'minigalaxy-dlc.json', 'gameinfo']
        exp = "dosbox"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    def test5_determine_launcher_type(self):
        files = ['thumbnail.jpg', 'docs', 'support', 'game', 'minigalaxy-dlc.json', 'gameinfo']
        exp = "final_resort"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    @mock.patch('shutil.which')
    def test6_determine_launcher_type(self, mock_shutil_which):
        mock_shutil_which.return_value = True
        files = ["CD", "CONFIG", "DATA", "DOS4GW.EXE", "DOSBOX", "DOSBox Configuration.lnk", "dosboxStonekeep.conf",
                 "dosboxStonekeep_settings.conf", "dosboxStonekeep_single.conf", "EULA.txt", "GameuxInstallHelper.dll",
                 "goggame-1207658671.dll", "goggame-1207658671.hashdb", "goggame-1207658671.ico",
                 "goggame-1207658671.info", "gog.ico", "Launch Settings.lnk", "Launch Stonekeep.lnk", "manual.pdf",
                 "PATCH", "prefix", "README.TXT", "SETUP.EXE", "SK.EXE", "Support.ico", "thumbnail.jpg", "unins000.dat",
                 "unins000.exe", "unins000.msg", "webcache.zip"]
        exp = "dosbox"
        obs = launcher.determine_launcher_type(files)
        self.assertEqual(exp, obs)

    @mock.patch('glob.glob')
    def test1_get_windows_exe_cmd(self, mock_glob):
        mock_glob.return_value = ["/test/install/dir/start.exe", "/test/install/dir/unins000.exe"]
        files = ['thumbnail.jpg', 'docs', 'support', 'game', 'minigalaxy-dlc.json', 'start.exe', 'unins000.exe']
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ["wine", "start.exe"]
        obs = launcher.get_windows_exe_cmd(game, files)
        self.assertEqual(exp, obs)

    def test1_get_dosbox_exe_cmd(self):
        files = ['thumbnail.jpg', 'docs', 'support', 'dosbox_bbb_single.conf', 'dosbox_aaa.conf', 'dosbox']
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ["dosbox", "-conf", "dosbox_aaa.conf", "-conf", "dosbox_bbb_single.conf", "-no-console", "-c", "exit"]
        obs = launcher.get_dosbox_exe_cmd(game, files)
        self.assertEqual(exp, obs)

    def test2_get_dosbox_exe_cmd(self):
        files = ["CD", "CONFIG", "DATA", "DOS4GW.EXE", "DOSBOX", "DOSBox Configuration.lnk", "dosboxStonekeep.conf",
                 "dosboxStonekeep_settings.conf", "dosboxStonekeep_single.conf", "EULA.txt", "GameuxInstallHelper.dll",
                 "goggame-1207658671.dll", "goggame-1207658671.hashdb", "goggame-1207658671.ico",
                 "goggame-1207658671.info", "gog.ico", "Launch Settings.lnk", "Launch Stonekeep.lnk", "manual.pdf",
                 "PATCH", "prefix", "README.TXT", "SETUP.EXE", "SK.EXE", "Support.ico", "thumbnail.jpg", "unins000.dat",
                 "unins000.exe", "unins000.msg", "webcache.zip"]
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ["dosbox", "-conf", "dosboxStonekeep.conf", "-conf", "dosboxStonekeep_single.conf", "-no-console", "-c",
               "exit"]
        obs = launcher.get_dosbox_exe_cmd(game, files)
        self.assertEqual(exp, obs)

    def test_get_scummvm_exe_cmd(self):
        files = ['thumbnail.jpg', 'data', 'docs', 'support', 'beneath.ini', 'scummvm', 'start.sh', 'gameinfo']
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ["scummvm", "-c", "beneath.ini"]
        obs = launcher.get_scummvm_exe_cmd(game, files)
        self.assertEqual(exp, obs)

    def test_get_start_script_exe_cmd(self):
        files = ['thumbnail.jpg', 'docs', 'support', 'game', 'start.sh', 'minigalaxy-dlc.json', 'gameinfo']
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ["/test/install/dir/start.sh"]
        obs = launcher.get_start_script_exe_cmd(game, files)
        self.assertEqual(exp, obs)

    @mock.patch('os.getcwd')
    @mock.patch('os.chdir')
    @mock.patch('subprocess.Popen')
    @mock.patch('minigalaxy.launcher.get_execute_command')
    def test1_run_game_subprocess(self, launcher_mock, mock_popen, mock_os_chdir, mock_os_getcwd):
        mock_process = "Mock Process"
        mock_popen.return_value = mock_process
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ("", mock_process)
        obs = launcher.run_game_subprocess(game)
        self.assertEqual(exp, obs)

    @mock.patch('os.getcwd')
    @mock.patch('os.chdir')
    @mock.patch('subprocess.Popen')
    @mock.patch('minigalaxy.launcher.get_execute_command')
    def test2_run_game_subprocess(self, launcher_mock, mock_popen, mock_os_chdir, mock_os_getcwd):
        mock_popen.side_effect = FileNotFoundError()
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ('No executable was found in /test/install/dir', None)
        obs = launcher.run_game_subprocess(game)
        self.assertEqual(exp, obs)

    @mock.patch('minigalaxy.launcher.check_if_game_start_process_spawned_final_process')
    def test1_check_if_game_started_correctly(self, mock_check_game):
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired("cmd", 1)
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = ""
        obs = launcher.check_if_game_started_correctly(mock_process, game)
        self.assertEqual(exp, obs)

    @mock.patch('minigalaxy.launcher.check_if_game_start_process_spawned_final_process')
    def test2_check_if_game_started_correctly(self, mock_check_game):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b"Output message", b"Error message")
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = "Error message"
        obs = launcher.check_if_game_started_correctly(mock_process, game)
        self.assertEqual(exp, obs)

    @mock.patch('os.getpid')
    @mock.patch('subprocess.check_output')
    def test1_check_if_game_start_process_spawned_final_process(self, mock_check_output, mock_getpid):
        mock_check_output.return_value = b"""UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 lis24 ?        00:00:02 /sbin/init splash
root         2     0  0 lis24 ?        00:00:00 [kthreadd]
root         3     2  0 lis24 ?        00:00:00 [rcu_gp]
root         4     2  0 lis24 ?        00:00:00 [rcu_par_gp]
root         6     2  0 lis24 ?        00:00:00 [kworker/0:0H-kblockd]
"""
        mock_getpid.return_value = 1000
        err_msg = "Error Message"
        game = Game("Test Game", install_dir="/test/install/dir")
        exp = err_msg
        obs = launcher.check_if_game_start_process_spawned_final_process(err_msg, game)
        self.assertEqual(exp, obs)

    @mock.patch('os.getpid')
    @mock.patch('subprocess.check_output')
    def test2_check_if_game_start_process_spawned_final_process(self, mock_check_output, mock_getpid):
        mock_check_output.return_value = b"""UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 lis24 ?        00:00:02 /sbin/init splash
root         2     0  0 lis24 ?        00:00:00 [kthreadd]
root         3     2  0 lis24 ?        00:00:00 [rcu_gp]
root         4     2  0 lis24 ?        00:00:00 [rcu_par_gp]
root         6     2  0 lis24 ?        00:00:00 [kworker/0:0H-kblockd]
makson    1006     2  0 lis24 ?        00:00:00 /bin/sh /home/makson/.paradoxlauncher/launcher-v2.2020.15/Paradox Launcher --pdxlGameDir /home/makson/GOG Games/Stellaris/game --gameDir /home/makson/GOG Games/Stellaris/game
"""
        mock_getpid.return_value = 1000
        err_msg = "Error Message"
        game = Game("Stellaris", install_dir="/home/makson/GOG Games")
        exp = ""
        obs = launcher.check_if_game_start_process_spawned_final_process(err_msg, game)
        self.assertEqual(exp, obs)
