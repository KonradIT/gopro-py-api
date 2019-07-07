import unittest
from goprocam import GoProCamera, constants
import time
# Assumes an up-to-date HERO5 Black is connected!!!

RESP_OK = '{}\n'
VALID_HERO5_MEDIA_PATH = 'http://10.5.5.9/videos/DCIM/'
SLEEP_SEC = 5


class MainTests(unittest.TestCase):

    def test_video_mode(self):
        print("VIDEO MODE")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(self.gopro.mode(constants.Mode.VideoMode), RESP_OK)

    def test_photo_mode(self):
        print("PHOTO MODE")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(self.gopro.mode(constants.Mode.PhotoMode,
                                         constants.Mode.SubMode.Photo.Single_H5), RESP_OK)

    def test_shutter(self):
        print("SHUTTER START")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(self.gopro.shutter(constants.start), RESP_OK)
        time.sleep(4)
        self.assertEqual(self.gopro.hilight(), RESP_OK)
        time.sleep(2)
        self.assertEqual(self.gopro.shutter(constants.stop), RESP_OK)

    def test_take_photo(self):
        print("take_photo()")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertIn(VALID_HERO5_MEDIA_PATH,
                      self.gopro.take_photo())

    def test_shoot_video(self):
        print("shoot_video(5)")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertIn(VALID_HERO5_MEDIA_PATH,
                      self.gopro.shoot_video(5))

    def test_power_off(self):
        print("POWER OFF")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(self.gopro.power_off(), RESP_OK)

    def test_power_on(self):
        print("POWER ON")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(self.gopro.power_on(), None)
        time.sleep(5)

    def test_recording_status(self):
        print("isRecording")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertEqual(
            self.gopro.IsRecording(), 0)

    def test_has_sd_card(self):
        print("Needs an SD card")
        time.sleep(SLEEP_SEC)
        self.gopro = GoProCamera.GoPro()
        self.assertFalse(
            self.gopro.getStatus(constants.Status.Status, constants.Status.STATUS.RemainingSpace) == 0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MainTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
