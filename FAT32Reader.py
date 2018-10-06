class FAT32Reader:
    def __init__(self, FAT32_path):
        self.FAT32_path = FAT32_path
        self.BPB = BPBReader32(FAT32_path)
        pass


class BPBReader:
    def __init__(self, FAT32_path):
        self.FAT32_path = FAT32_path
        self.jmpBoot = None
        self.OEMName = None
        self.BytesPerSec = None
        self.SecPerClus = None
        self.ResvdSecCnt = None
        self.NumFATs = None
        self.RootEntCnt = None
        self.TotSec16 = None
        self.Media = None
        self.FATSz16 = None
        self.SecPerTrk = None
        self.NumHeads = None
        self.HiddSec = None
        self.TotSec32 = None
        with open(FAT32_path, "rb") as f:
            self.get_common_bpb_structure(f)

    def get_common_bpb_structure(self, f):
        self.jmpBoot = f.read(3)
        self.OEMName = f.read(8)
        self.BytesPerSec = f.read(2)
        self.SecPerClus = f.read(1)
        self.ResvdSecCnt = f.read(2)
        self.NumFATs = f.read(1)
        self.RootEntCnt = f.read(2)
        self.TotSec16 = f.read(2)
        self.Media = f.read(1)
        self.FATSz16 = f.read(2)
        self.SecPerTrk = f.read(2)
        self.NumHeads = f.read(2)
        self.HiddSec = f.read(4)
        self.TotSec32 = f.read(4)


class BPBReader32(BPBReader):
    def __init__(self, FAT32_path):
        super(BPBReader32, self).__init__(FAT32_path)
        self.FATSz32 = None
        self.ExtFlags = None
        self.FSVer = None
        self.RootClus = None
        self.FSInfo = None
        self.BkBootSec = None
        self.Reserved = None
        self.DrvNum = None
        self.Reserved1 = None
        self.BootSig = None
        self.VolID = None
        self.VolLab = None
        self.FilSysType = None
        with open(FAT32_path, "rb") as f:
            f.seek(36)
            self.get_fat32_bpb_structure(f)
        self.DataSec = int.from_bytes(self.TotSec32, byteorder="little") -\
                       (int.from_bytes(self.ResvdSecCnt, byteorder="little")
                        + int.from_bytes(self.NumFATs, byteorder="little")*int.from_bytes(self.FATSz32, byteorder="little"))

        self.CountOfClusters = int(self.DataSec / int.from_bytes(self.SecPerClus, byteorder="little"))
        if self.CountOfClusters < 65525:
            raise Exception("That's not a FAT32!")

    def get_fat32_bpb_structure(self, f):
        self.FATSz32 = f.read(4)
        self.ExtFlags = f.read(2)
        self.FSVer = f.read(2)
        self.RootClus = f.read(4)
        self.FSInfo = f.read(2)
        self.BkBootSec = f.read(2)
        self.Reserved = f.read(12)
        self.DrvNum = f.read(1)
        self.Reserved1 = f.read(1)
        self.BootSig = f.read(1)
        self.VolID = f.read(4)
        self.VolLab = f.read(11)
        self.FilSysType = f.read(8)
