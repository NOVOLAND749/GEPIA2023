import GeneDetailType from "~/types/GeneDetailType";

const getEnsemblBase = (gene: GeneDetailType) => gene.ENSEMBL.split(".")[0];

const getGeneCardLink = (gene: GeneDetailType) => {
  return `//www.genecards.org/cgi-bin/carddisp.pl?gene=${gene.gene_name}`;
};

const getNCBILink = (gene: GeneDetailType) => {
  return `//www.ncbi.nlm.nih.gov/gene/?term=${getEnsemblBase(gene)}`;
};

const getEnsemblLink = (gene: GeneDetailType) => {
  return `//www.ensembl.org/Homo_sapiens/Gene/Summary?g=${gene.gene_name}`;
};

const getEBILink = (gene: GeneDetailType) => {
  return `//www.ebi.ac.uk/gxa/query?geneQuery=${gene.gene_name}`;
};

const getOMIMLink = (gene: GeneDetailType) => {
  return `//omim.org/search/?search=${gene.gene_name}`;
};

const getCOSMICLink = (gene: GeneDetailType) => {
  return `//cancer.sanger.ac.uk/cosmic/gene/analysis?ln=${gene.gene_name}`;
};

const getHPALink = (gene: GeneDetailType) => {
  return `//www.proteinatlas.org/${getEnsemblBase(gene)}-${
    gene.gene_name
  }/tissue`;
};

const getDrugBankLink = (gene: GeneDetailType) => {
  return `//www.drugbank.ca/unearth/q?searcher=bio_entities&query=${gene.gene_name}`;
};

export default function getGeneExternalLinks(gene: GeneDetailType) {
  return [
    { name: "GeneCard", link: getGeneCardLink(gene) },
    { name: "NCBI", link: getNCBILink(gene) },
    { name: "Ensembl", link: getEnsemblLink(gene) },
    { name: "EBI", link: getEBILink(gene) },
    { name: "OMIM", link: getOMIMLink(gene) },
    { name: "COSMIC", link: getCOSMICLink(gene) },
    { name: "HPA", link: getHPALink(gene) },
    { name: "DrugBank", link: getDrugBankLink(gene) },
  ];
}
