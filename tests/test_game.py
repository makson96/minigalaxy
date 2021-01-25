import unittest
import sys
from unittest.mock import MagicMock, mock_open, patch
m_config = MagicMock()
sys.modules['minigalaxy.config'] = m_config
from minigalaxy import filesys_utils
from minigalaxy.game import Game


class TestGame(unittest.TestCase):
    def test_strip_within_comparison(self):
        game1 = Game("!@#$%^&*(){}[]\"'_-<>.,;:")
        game2 = Game("")
        game3 = Game("hallo")
        game4 = Game("Hallo")
        game5 = Game("Hallo!")
        self.assertEqual(game1, game2)
        self.assertNotEqual(game2, game3)
        self.assertEqual(game3, game4)
        self.assertEqual(game3, game5)

    def test_local_and_api_comparison(self):
        larry1_api = Game("Leisure Suit Larry 1 - In the Land of the Lounge Lizards", game_id=1207662033)
        larry1_local_gog = Game("Leisure Suit Larry", install_dir="/home/user/Games/Leisure Suit Larry",
                                game_id=1207662033)
        larry1_local_minigalaxy = Game("Leisure Suit Larry",
                                       install_dir="/home/wouter/Games/Leisure Suit Larry 1 - In the Land of the Lounge Lizards",
                                       game_id=1207662033)

        self.assertEqual(larry1_local_gog, larry1_local_minigalaxy)
        self.assertEqual(larry1_local_minigalaxy, larry1_api)
        self.assertEqual(larry1_local_gog, larry1_api)

        larry2_api = Game("Leisure Suit Larry 2 - Looking For Love (In Several Wrong Places)", game_id=1207662053)
        larry2_local_minigalaxy = Game("Leisure Suit Larry 2",
                                       install_dir="/home/user/Games/Leisure Suit Larry 2 - Looking For Love (In Several Wrong Places)",
                                       game_id=1207662053)
        larry2_local_gog = Game("Leisure Suit Larry 2", install_dir="/home/user/Games/Leisure Suit Larry 2",
                                game_id=1207662053)

        self.assertNotEqual(larry1_api, larry2_api)
        self.assertNotEqual(larry2_local_gog, larry1_api)
        self.assertNotEqual(larry2_local_gog, larry1_local_gog)
        self.assertNotEqual(larry2_local_gog, larry1_local_minigalaxy)
        self.assertNotEqual(larry2_local_minigalaxy, larry1_api)
        self.assertNotEqual(larry2_local_minigalaxy, larry1_local_minigalaxy)

    def test_local_comparison(self):
        larry1_local_gog = Game("Leisure Suit Larry", install_dir="/home/user/Games/Leisure Suit Larry",
                                game_id=1207662033)
        larry1_vga_local_gog = Game("Leisure Suit Larry VGA", install_dir="/home/user/Games/Leisure Suit Larry VGA",
                                    game_id=1207662043)

        self.assertNotEqual(larry1_local_gog, larry1_vga_local_gog)

    def test1_is_update_available(self):
        game = Game("Version Test game")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {'version': 'gog-2'}
        expected = True
        observed = game.is_update_available("gog-3")
        self.assertEqual(expected, observed)

    def test2_is_update_available(self):
        game = Game("Version Test game")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {'version': "91.8193.16"}
        expected = False
        observed = game.is_update_available("91.8193.16")
        self.assertEqual(expected, observed)

    def test3_is_update_available(self):
        game = Game("Version Test game")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {'version': "91.8193.16", "dlcs": {"Neverwinter Nights: Wyvern Crown of Cormyr": {"version": "82.8193.20.1"}}}
        expected = True
        observed = game.is_update_available("91.8193.16", dlc_title="Neverwinter Nights: Wyvern Crown of Cormyr")
        self.assertEqual(expected, observed)

    def test4_is_update_available(self):
        game = Game("Version Test game")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {'version': "91.8193.16", "dlcs": {"Neverwinter Nights: Wyvern Crown of Cormyr": {"version": "82.8193.20.1"}}}
        expected = False
        observed = game.is_update_available("82.8193.20.1", dlc_title="Neverwinter Nights: Wyvern Crown of Cormyr")
        self.assertEqual(expected, observed)

    def test5_is_update_available(self):
        game = Game("Version Test game")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {'version': "91.8193.16", "dlcs": {}}
        game.legacy_get_dlc_status = MagicMock()
        game.legacy_get_dlc_status.return_value = "updatable"
        expected = True
        observed = game.is_update_available("82.8193.20.1", dlc_title="Neverwinter Nights: Wyvern Crown of Cormyr")
        self.assertEqual(expected, observed)

    def test1_get_install_directory_name(self):
        game = Game("Get Install Directory Test1")
        expected = "Get Install Directory Test1"
        observed = game.get_install_directory_name()
        self.assertEqual(expected, observed)

    def test2_get_install_directory_name(self):
        game = Game("Get\r Install\n Directory Test2!@#$%")
        expected = "Get Install Directory Test2"
        observed = game.get_install_directory_name()
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test1_fallback_read_installed_version(self, mock_isfile):
        mock_isfile.return_value = True
        gameinfo = """Beneath A Steel Sky
gog-2
20150
en-US
1207658695
1207658695
664777434"""
        game = Game("Game Name test1")
        expected = "gog-2"
        with patch("builtins.open", mock_open(read_data=gameinfo)):
            observed = game.fallback_read_installed_version()
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test2_fallback_read_installed_version(self, mock_isfile):
        mock_isfile.return_value = False
        gameinfo = """Beneath A Steel Sky
    gog-2
    20150
    en-US
    1207658695
    1207658695
    664777434"""
        game = Game("Game Name test2")
        expected = "0"
        with patch("builtins.open", mock_open(read_data=gameinfo)):
            observed = game.fallback_read_installed_version()
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test1_legacy_get_dlc_status(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "not-installed", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "updatable", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {}]'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test1")
            game.read_installed_version = MagicMock()
            game.installed_version = "1"
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Wyvern Crown of Cormyr", "")
        expected = "not-installed"
        observed = dlc_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test2_legacy_get_dlc_status(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "not-installed", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "updatable", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {}]'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Infinite Dungeons", "")
        expected = "updatable"
        observed = dlc_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test3_legacy_get_dlc_status(self, mock_isfile):
        mock_isfile.side_effect = [False]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "not-installed", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "updatable", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {}]'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Infinite Dungeons", "")
        expected = "not-installed"
        observed = dlc_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch("minigalaxy.filesys_utils._check_if_accordance_with_lists")
    @unittest.mock.patch('os.path.isfile')
    def test1_set_info(self, mock_isfile, m_check_if_accordance_with_lists):
        mock_isfile.return_value = True
        m_check_if_accordance_with_lists.return_value = ""
        json_content = '{"version": "gog-2"}'
        with patch("builtins.open", mock_open(read_data=json_content)) as m:
            game = Game("Game Name test2")
            game.set_info("version", "gog-3")
        mock_c = m.mock_calls
        write_string = ""
        for kall in mock_c:
            name, args, kwargs = kall
            if name == "().write":
                write_string = "{}{}".format(write_string, args[0])
        expected = '{"version": "gog-3"}'
        observed = write_string
        self.assertEqual(expected, observed)

    @unittest.mock.patch("minigalaxy.filesys_utils._check_if_accordance_with_lists")
    @unittest.mock.patch('os.path.isfile')
    def test2_set_dlc_info(self, mock_isfile, m_check_if_accordance_with_lists):
        mock_isfile.return_value = False
        m_check_if_accordance_with_lists.return_value = ""
        dlc_name = "Neverwinter Nights: Wyvern Crown of Cormyr"
        with patch("builtins.open", mock_open()) as m:
            game = Game("Neverwinter Nights")
            game.set_dlc_info("version", "82.8193.20.1", dlc_name)
        mock_c = m.mock_calls
        write_string = ""
        for kall in mock_c:
            name, args, kwargs = kall
            if name == "().write":
                write_string = "{}{}".format(write_string, args[0])
        expected = '{"dlcs": {"Neverwinter Nights: Wyvern Crown of Cormyr": {"version": "82.8193.20.1"}}}'
        observed = write_string
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test1_get_dlc_status_version(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "not-installed", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "installed", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {"Neverwinter Nights: Wyvern Crown of Cormyr": ' \
                       '"81.8193.16", "Neverwinter Nights: Infinite Dungeons": "81.8193.17", "Neverwinter Nights: ' \
                       'Pirates of the Sword Coast": "81.8193.18"}] '
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Infinite Dungeons", "81.8193.16")
        expected = "updatable"
        observed = dlc_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test2_get_dlc_status_version(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "updatable", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "installed", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {"Neverwinter Nights: Wyvern Crown of Cormyr": ' \
                       '"81.8193.16", "Neverwinter Nights: Infinite Dungeons": "81.8193.17", "Neverwinter Nights: ' \
                       'Pirates of the Sword Coast": "81.8193.18"}] '
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Wyvern Crown of Cormyr", "")
        expected = "updatable"
        observed = dlc_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test3_get_dlc_status_version(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '[{"Neverwinter Nights: Wyvern Crown of Cormyr": "updatable", ' \
                       '"Neverwinter Nights: Infinite Dungeons": "installed", "Neverwinter Nights: Pirates of ' \
                       'the Sword Coast": "installed"}, {"Neverwinter Nights: Wyvern Crown of Cormyr": ' \
                       '"81.8193.16", "Neverwinter Nights: Infinite Dungeons": "81.8193.17", "Neverwinter Nights: ' \
                       'Pirates of the Sword Coast": "81.8193.18"}] '
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            dlc_status = game.legacy_get_dlc_status("Neverwinter Nights: Infinite Dungeons", "81.8193.17")
        expected = "installed"
        observed = dlc_status
        self.assertEqual(expected, observed)

    def test_get_stripped_name(self):
        name_string = "Beneath A Steel Sky"
        game = Game(name_string)
        expected = "BeneathASteelSky"
        observed = game.get_stripped_name()
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test1_load_minigalaxy_info_json(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '{"version": "gog-2"}'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            jscon_dict = game.load_minigalaxy_info_json()
        expected = {"version": "gog-2"}
        observed = jscon_dict
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test2_load_minigalaxy_info_json(self, mock_isfile):
        mock_isfile.side_effect = [False]
        json_content = '{"version": "gog-2"}'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test2")
            jscon_dict = game.load_minigalaxy_info_json()
        expected = {}
        observed = jscon_dict
        self.assertEqual(expected, observed)

    @unittest.mock.patch("minigalaxy.filesys_utils._check_if_accordance_with_lists")
    def test_save_minigalaxy_info_json(self, m_check_if_accordance_with_lists):
        m_check_if_accordance_with_lists.return_value = ""
        json_dict = {"version": "gog-2"}
        with patch("builtins.open", mock_open()) as m:
            game = Game("Neverwinter Nights")
            game.save_minigalaxy_info_json(json_dict)
        mock_c = m.mock_calls
        write_string = ""
        for kall in mock_c:
            name, args, kwargs = kall
            if name == "().write":
                write_string = "{}{}".format(write_string, args[0])
        expected = '{"version": "gog-2"}'
        observed = write_string
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.exists')
    def test1_is_installed(self, mock_isfile):
        mock_isfile.side_effect = [False]
        game = Game("Game Name Test")
        game.load_minigalaxy_info_json = MagicMock()
        exp = False
        obs = game.is_installed()
        self.assertEqual(exp, obs)

    @unittest.mock.patch('os.path.exists')
    def test3_is_installed(self, mock_isfile):
        mock_isfile.side_effect = [True]
        game = Game("Game Name Test", install_dir="Test Install Dir")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {"dlcs": {"Neverwinter Nights: Wyvern Crown of Cormyr": {"version": "82.8193.20.1"}}}
        exp = True
        obs = game.is_installed(dlc_title="Neverwinter Nights: Wyvern Crown of Cormyr")
        self.assertEqual(exp, obs)

    @unittest.mock.patch('os.path.exists')
    def test4_is_installed(self, mock_isfile):
        mock_isfile.side_effect = [True]
        game = Game("Game Name Test", install_dir="Test Install Dir")
        game.load_minigalaxy_info_json = MagicMock()
        game.load_minigalaxy_info_json.return_value = {"dlcs": {"Neverwinter Nights: Wyvern Crown of Cormyr": {"version": "82.8193.20.1"}}}
        game.legacy_get_dlc_status = MagicMock()
        game.legacy_get_dlc_status.return_value = "not-installed"
        exp = False
        obs = game.is_installed(dlc_title="Not Present DLC")
        self.assertEqual(exp, obs)

    @unittest.mock.patch('os.path.isfile')
    def test_get_info(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '{"example_key": "example_value"}'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test")
            game_get_status = game.get_info("example_key")
        expected = "example_value"
        observed = game_get_status
        self.assertEqual(expected, observed)

    @unittest.mock.patch('os.path.isfile')
    def test_get_dlc_info(self, mock_isfile):
        mock_isfile.side_effect = [True]
        json_content = '{"dlcs": {"example_dlc" : {"example_key": "example_value"}}}'
        with patch("builtins.open", mock_open(read_data=json_content)):
            game = Game("Game Name test")
            game_get_status = game.get_dlc_info("example_key", "example_dlc")
        expected = "example_value"
        observed = game_get_status
        self.assertEqual(expected, observed)

    def test1_set_install_dir(self):
        m_config.Config.get.return_value = "/home/user/GOG Games"
        game = Game("Neverwinter Nights")
        game.set_install_dir()
        exp = "/home/user/GOG Games/Neverwinter Nights"
        obs = game.install_dir
        self.assertEqual(exp, obs)

    def test2_set_install_dir(self):
        m_config.Config.get.return_value = "/home/user/GOG Games"
        game = Game("Neverwinter Nights")
        game.set_install_dir()
        exp = "/home/user/GOG Games/Neverwinter Nights/minigalaxy-info.json"
        obs = game.status_file_path
        self.assertEqual(exp, obs)


del sys.modules["minigalaxy.config"]
del sys.modules["minigalaxy.game"]
del sys.modules["minigalaxy.filesys_utils"]
