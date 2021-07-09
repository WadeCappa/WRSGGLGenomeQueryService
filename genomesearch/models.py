from genomesearch import db


class Genome(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    SNPId = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    chrom = db.Column(db.String(5), nullable=True)
    cM = db.Column(db.Float, nullable=False)
    AAFreq = db.Column(db.Float, nullable=False)
    ABFreq = db.Column(db.Float, nullable=False)
    BBFreq = db.Column(db.Float, nullable=False)
    SNP = db.Column(db.String(10), nullable=False)
    alleleA = db.Column(db.String(2), nullable=True)
    alleleB = db.Column(db.String(2), nullable=True)
    sourceSeq = db.Column(db.Text(120), nullable=False)
    samples = db.Column(db.Text(500), nullable=False)


    def __init__(self, SNPId=None, name=None, chrom = None, cM=None, AAFreq = None, ABFreq = None, BBFreq = None, SNP = None, alleleA = None, alleleB = None, sourceSeq = None, samples=None):
        self.SNPId = SNPId
        self.name = name
        self.chrom = chrom
        self.cM = cM 
        self.AAFreq = AAFreq
        self.ABFreq = ABFreq
        self.BBFreq = BBFreq
        self.SNP = SNP
        self.alleleA = alleleA
        self.alleleB = alleleB
        self.sourceSeq = sourceSeq
        self.samples = samples

    def __repr__(self):
        return f"Genome('{self.SNPId}','{self.name}', '{self.chrom}', '{self.cM}', '{self.AAFreq}', '{self.ABFreq}', '{self.BBFreq}', '{self.SNP}', '{self.SNP}', '{self.alleleA}', '{self.alleleB}', '{self.sourceSeq}', '{self.samples}')"