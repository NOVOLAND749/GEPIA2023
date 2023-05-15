export default interface GeneDetailType {
  id: number;
  gene_name: string;
  ENSEMBL: string;
  description: string;
  Synonyms: string;
  chromosome: string;
  start: number;
  end: number;
}
