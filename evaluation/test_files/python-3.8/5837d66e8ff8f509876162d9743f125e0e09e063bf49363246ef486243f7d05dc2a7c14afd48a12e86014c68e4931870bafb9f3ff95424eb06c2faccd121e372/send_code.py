import logging
from telectron import raw
from telectron import types
from telectron.errors import PhoneMigrate, NetworkMigrate
from telectron.scaffold import Scaffold
from telectron.session import Session, Auth
log = logging.getLogger(__name__)

class SendCode(Scaffold):

    async def send_code(self, phone_number: str) -> 'types.SentCode':
        """Send the confirmation code to the given phone number.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

        Returns:
            :obj:`~telectron.types.SentCode`: On success, an object containing information on the sent confirmation code
            is returned.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = phone_number.strip(' +')
        while True:
            try:
                r = await self.send(raw.functions.auth.SendCode(phone_number=phone_number, api_id=self.api_id, api_hash=self.api_hash, settings=raw.types.CodeSettings()))
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()
                await self.storage.dc_id(e.x)
                await self.storage.auth_key(await Auth(self, await self.storage.dc_id(), await self.storage.test_mode()).create())
                self.session = Session(self, await self.storage.dc_id(), await self.storage.auth_key(), await self.storage.test_mode())
                await self.session.start()
            else:
                return types.SentCode._parse(r)