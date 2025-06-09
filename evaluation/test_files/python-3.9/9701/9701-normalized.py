def toHdlConversion(self, top, topName: str, saveTo: str) -> List[str]:
    """
        :param top: object which is represenation of design
        :param topName: name which should be used for ipcore
        :param saveTo: path of directory where generated files should be stored

        :return: list of file namens in correct compile order
        """
    return toRtl(top, saveTo=saveTo, name=topName, serializer=self.serializer, targetPlatform=self.targetPlatform)